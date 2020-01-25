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
    fig : plotly.graph_objects.Figure
        Bar chart showing the number of remaining items.

    """
    # calculate height of plot
    height = len(remaining) * 30

    data = go.Bar(
        x=remaining.values,
        y=remaining.index,
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

    fig = go.Figure(
        data=data,
        layout=layout
    )

    return fig


def plot_timeline(purch_per_day):
    """Plot a timeline that shows number of purchases per day.

    Parameters
    ----------
    purch_per_day : pandas.Series
      Series object containing the number of purchases per day.
      Index needs to be of time series type.

    Returns
    -------
    fig : plotly.graph_objects.Figure
      Scatter plot showing the number of purchases per day.

    """
    data = go.Scatter(
        x=purch_per_day.index,
        y=purch_per_day.values,
        mode='lines+markers'
    )

    layout = go.Layout(
        xaxis=dict(title='Zeit',
                   titlefont=dict(size=20),
                   tickfont=dict(size=15),
                   mirror=True,
                   ticks='outside',
                   showline=False,
                   linewidth=1,
                   ),
        yaxis=dict(title='Käufe',
                   titlefont=dict(size=20),
                   tickfont=dict(size=15),
                   mirror=False,
                   showline=True,
                   linewidth=1,
                   ),
        margin={'t': 0, 'b': 10, 'l': 50, 'r': 0},
        showlegend=False,
        hoverlabel=dict(font=dict(size=20)),
        xaxis_rangeslider_visible=True
    )

    fig = go.Figure(
        data=data,
        layout=layout
    )

    return fig
