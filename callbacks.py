"""Callbacks for the main app."""
import pandas as pd
import plot_utils
from app import app
from dash.dependencies import Input, Output


@app.callback(
    Output("shared_data", "children"),
    [Input("interval-component", "n_intervals")]
)
def update_data(n_intervals):
    """Update the purchase data in regular intervals.

    Update interval is controlled by the interval component.

    Parameters
    ----------
    n_intervals : int
        Number of passed intervals.

    Returns
    -------
    full_data : str
        JSON serialized pandas data frame containing purchase data.

    """
    # read individual data files
    purchases = pd.read_csv(
        "./assets/purchase.txt",
        header=None,
        names=['date', 'name', 'barcode', 'paid']
    )

    products = pd.read_csv(
        "./assets/produkt.txt",
        header=None,
        names=['id', 'barcode', 'product', 'price', 'stock']
    )

    # combine data files into a single data frame
    full_data = purchases.merge(
        products,
        on='barcode',
        # retain rows for never purchased products to make the inventory work
        how='outer',
    ).reindex(
        columns=['date', 'name', 'barcode',
                 'paid', 'product', 'price', 'stock']
    )

    full_data["date"] = pd.to_datetime(full_data["date"])

    full_data = full_data.to_json()

    return full_data


@app.callback(
    Output("debt_table", "data"),
    [Input("shared_data", "children")]
)
def update_debts(shared_data):
    """Update debt table.

    Parameters
    ----------
    shared_data : str
        JSON serialized pandas data frame containing purchase data.

    Returns
    -------
    debts : dict
        Debt table.

    """
    df = pd.read_json(shared_data)

    debts = df[df["paid"] == 0].groupby(["name"])["price"].agg("sum")
    debts = debts.sort_values(ascending=False)
    debts = debts.reset_index()

    return debts.to_dict("records")


@app.callback(
    [Output("info-box-revenue-title", "children"),
     Output("info-box-revenue-value", "children")],
    [Input("shared_data", "children")]
)
def update_revenue(shared_data):
    """Update revenue summary.

    Parameters
    ----------
    shared_data : str
        JSON serialized pandas data frame containing purchase data.

    Returns
    -------
    title : str
        Title of the info box.
    value : str
        Value of the info box.

    """
    df = pd.read_json(shared_data)

    date = df["date"].min().date()
    revenue = df.dropna()['price'].sum()

    title = "Umsatz seit {}".format(date.strftime("%d.%m.%Y"))
    value = "{:.2f} €".format(revenue)

    return title, value


@app.callback(
    Output("info-box-royal-value", "children"),
    [Input("shared_data", "children")]
)
def update_royal(shared_data):
    """Update info box for the person with the most drinks.

    Parameters
    ----------
    shared_data : str
        JSON serialized pandas data frame containing purchase data.

    Returns
    -------
    value : str
        Value of the info box.

    """
    df = pd.read_json(shared_data)
    counts = df['name'].value_counts()

    value = "{:s} ({:d} St.)".format(counts.idxmax(), counts.max())

    return value


@app.callback(
    Output("info-box-bestseller-value", "children"),
    [Input("shared_data", "children")]
)
def update_bestseller(shared_data):
    """Update info box for the person with the most drinks.

    Parameters
    ----------
    shared_data : str
        JSON serialized pandas data frame containing purchase data.

    Returns
    -------
    value : str
        Value of the info box.

    """
    df = pd.read_json(shared_data)

    this_month = pd.Timestamp.now().month

    mask = (df['date'].dt.month == this_month)
    counts = df[mask].groupby("product")["name"].count()
    try:
        value = counts.idxmax()
    except ValueError:
        value = "N/A"

    return value


@app.callback(
    Output('timeline', 'figure'),
    [Input('shared_data', 'children')]
)
def update_timeline(shared_data):
    """Update timeline plot.

    Parameters
    ----------
    shared_data : str
        JSON serialized pandas data frame containing purchase data.

    Returns
    -------
    plot : plotly.graph_objects.Figure
        Scatter plot showing the number of purchases per day.

    """
    df = pd.read_json(shared_data)

    purch_per_day = df['date'].dt.floor('d').value_counts().sort_index()
    fig = plot_utils.plot_timeline(purch_per_day)

    return fig


@app.callback(
    Output("inventory", "figure"),
    [Input("shared_data", "children")]
)
def update_inventory(shared_data):
    """Update inventory chart.

    Parameters
    ----------
    shared_data : str
        JSON serialized pandas data frame containing purchase data.

    Returns
    -------
    plot : plotly.graph_objects.Figure
        Bar chart showing the number of remaining items.

    """
    df = pd.read_json(shared_data)

    stock = df.groupby('product')['stock'].first()
    remaining = stock.sort_index(ascending=False)

    plot = plot_utils.plot_inventory_chart(remaining)

    return plot


@app.callback(
    Output("statistics", "figure"),
    [Input("shared_data", "children")]
)
def update_chart(shared_data):
    """Update inventory chart.

    Parameters
    ----------
    shared_data : str
        JSON serialized pandas data frame containing purchase data.

    Returns
    -------
    plot : plotly.graph_objects.Figure
        Bar chart showing the number of remaining items.

    """
    df = pd.read_json(shared_data)
    grouped_df = df.groupby(['name', 'product']).size()

    plot = plot_utils.plot_statistics_chart(grouped_df)

    return plot
