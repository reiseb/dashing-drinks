"""Plotting utilities."""
import plotly.graph_objects as go


def plot_inventory_chart(remaining):
    """Update inventory chart.

    Parameters
    ----------
    remaining : pandas.Series
        Series object containing the number of remaining items
        for each product category.

    Returns
    -------
    plot : plotly.graph_objects.Figure
        Bar chart showing the number of remaining items.

    """
    # calculate height of plot
    height = len(remaining) * 30

    data = go.Bar(
        x=remaining.values,
        y=remaining.index.values,
        orientation='h',
    ),

    layout = go.Layout(
        xaxis=dict(title='Anzahl',
                   titlefont=dict(size=20),
                   tickfont=dict(size=15),
                   mirror=True,
                   ticks='outside',
                   showline=False,
                   linewidth=1,
                   ),
        yaxis=dict(title='',
                   titlefont=dict(size=20),
                   tickfont=dict(size=15),
                   mirror=False,
                   showline=True,
                   linewidth=1,
                   ),
        margin={'t': 0, 'b': 0, 'l': 200, 'r': 0},
        showlegend=False,
        hoverlabel=dict(font=dict(size=20)),
        height=height,
    )

    plot = go.Figure(
        data=data,
        layout=layout
    )

    return plot
