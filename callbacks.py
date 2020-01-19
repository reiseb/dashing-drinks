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
