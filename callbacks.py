"""Callbacks for the main app."""
import os

import pandas as pd
from dash.dependencies import Input, Output

from . import plot_utils


def register_callbacks(dashapp):
    """Register callbacks with the dash server."""
    @dashapp.callback(
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
            os.getenv("PURCHASE_FILE"),
            header=None,
            names=['date', 'name', 'barcode', 'paid']
        )

        products = pd.read_csv(
            os.getenv("PRODUCT_FILE"),
            header=None,
            names=['id', 'barcode', 'product', 'price', 'stock']
        )

        # combine data files into a single data frame
        full_data = purchases.merge(
            products,
            on='barcode',
            # retain rows for never purchased products to make the
            # inventory work
            how='outer',
        ).reindex(
            columns=['date', 'name', 'barcode',
                     'paid', 'product', 'price', 'stock']
        )

        full_data["date"] = pd.to_datetime(full_data["date"])

        full_data = full_data.to_json()

        return full_data

    @dashapp.callback(
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

    @dashapp.callback(
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

    @dashapp.callback(
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

    @dashapp.callback(
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
        counts = df[mask].groupby("product").size()
        try:
            value = counts.idxmax()
        except ValueError:
            value = "N/A"

        return value

    @dashapp.callback(
        Output('timeline', 'figure'),
        [Input('shared_data', 'children'),
         Input('filter_time_by', 'value')]
    )
    def update_timeline(shared_data, filter_by):
        """Update timeline plot.

        Parameters
        ----------
        shared_data : str
            JSON serialized pandas data frame containing purchase data.
        filter_time_by : str
            One of the following options:
                - ''
                - 'month'
                - 'weekday'
                - 'hour'

        Returns
        -------
        plot : plotly.graph_objects.Figure
            Scatter plot showing the number of purchases per day.

        """
        df = pd.read_json(shared_data)

        # no filter -> default to timeline
        if filter_by == 'no_filter':
            purch = df.groupby(df['date'].dt.date).size()
            fig = plot_utils.plot_timeline(purch)
            return fig

        # apply various filters
        elif filter_by == 'hour':
            purch = df.groupby(df['date'].dt.hour).size()
        elif filter_by == 'weekday':
            purch = df.groupby(df['date'].dt.day_name('de_DE.UTF-8')).size()
            sort_mask = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag',
                         'Freitag', 'Samstag', 'Sonntag']
            purch = purch.reindex(sort_mask)
        elif filter_by == 'month':
            purch = df.groupby(df['date'].dt.month_name('de_DE.UTF-8')).size()
            sort_mask = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                         'Juli', 'August', 'September', 'Oktober', 'November',
                         'Dezember']
            purch = purch.reindex(sort_mask)
        else:
            raise ValueError('Unknown filter {}'.format(filter_by))

        fig = plot_utils.plot_purch_per_time(purch, filter_by)

        return fig

    @dashapp.callback(
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

        stock = df.groupby('product')[['stock', 'price']].first()
        remaining = stock.sort_index(ascending=False)

        plot = plot_utils.plot_inventory_chart(remaining)

        return plot

    @dashapp.callback(
        Output("statistics", "figure"),
        [Input("shared_data", "children"),
         Input("stats_switch", "value")]
    )
    def update_chart(shared_data, relative_drinks):
        """Update inventory chart.

        Parameters
        ----------
        shared_data : str
            JSON serialized pandas data frame containing purchase data.
        relative_drinks : boolean
            True to show number of each drink per each person.

        Returns
        -------
        plot : plotly.graph_objects.Figure
            Bar chart showing the number of remaining items.

        """
        df = pd.read_json(shared_data)

        # How many drinks of each product did a person have?
        grouped_df = df.groupby(["name", "product"]).size()

        # Product names of all consumed products
        products = grouped_df.groupby("product").groups.keys()

        # Total number of drinks per person
        abs_drinks_per_person = grouped_df.groupby(level=0).sum().sort_values()

        # calculate percentage of each drink for each person
        rel_drinks_per_person = {}
        for product in products:
            drinks = grouped_df[:, product].divide(abs_drinks_per_person)
            # sort by total number of drinks per person
            drinks = drinks.reindex(abs_drinks_per_person.index)
            rel_drinks_per_person[product] = drinks

        if relative_drinks:
            plot = plot_utils.plot_rel_drinks_per_person(rel_drinks_per_person)
        else:
            plot = plot_utils.plot_abs_drinks_per_person(abs_drinks_per_person)

        return plot
