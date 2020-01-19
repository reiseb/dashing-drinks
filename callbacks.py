"""Callbacks for the main app."""
import pandas as pd
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
        names=['date', 'name', 'barcode']
    )

    products = pd.read_csv(
        "./assets/produkt.txt",
        header=None,
        names=['id', 'barcode', 'product', 'price']
    )

    # combine data files into a single data frame
    full_data = purchases.merge(
        products,
        left_on='barcode',
        right_on='barcode'
    ).reindex(
        columns=['date', 'name', 'barcode', 'product', 'price']
    )

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
    purch = pd.read_json(shared_data)

    debts = purch.groupby(["name"])["price"].agg("sum")
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
    purch = pd.read_json(shared_data)

    date = pd.to_datetime(purch["date"]).min().date()
    revenue = purch["price"].sum()

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
    purch = pd.read_json(shared_data)
    counts = purch.groupby("name")["product"].count()
    royal = counts.idxmax()
    return royal
