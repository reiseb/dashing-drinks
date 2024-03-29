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
        x=remaining['stock'].values,
        y=remaining.index,
        customdata=remaining['price'],
        orientation='h',
        hovertemplate='<b>%{y}</b><br>%{x} Stück<br>%{customdata:.2f} EUR<extra></extra>',
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
        mode='lines+markers',
        hovertemplate='<b>%{x}</b><br>%{y} Käufe<extra></extra>',
        line_width=3,
        marker_size=8,
    )

    layout = go.Layout(
        xaxis=dict(title='Datum',
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


def plot_purch_per_time(purch, x_type):
    """Plot a bar chart that shows number of purchases per hour.

    Parameters
    ----------
    purch : pandas.Series
      Series object containing the number of purchases per time.
      Index needs to be of time series type.
    x_type : str
        One of the following:
            - month
            - weekday
            - hour

    Returns
    -------
    fig : plotly.graph_objects.Figure
      Bar plot showing the number of purchases per hour.

    """
    if x_type == 'hour':
        customdata = purch.index + 1
        hovertemplate = (
            '<b>%{x:.2f}-%{customdata:.2f} Uhr</b><br>'
            + '%{y:d} Stück<extra></extra>'
        )
    else:
        customdata = None
        hovertemplate = '<b>%{x}</b><br>%{y} Käufe<extra></extra>'

    data = go.Bar(
        x=purch.index,
        y=purch.values,
        customdata=customdata,
        hovertemplate=hovertemplate
    )

    layout = go.Layout(
        xaxis=dict(title='',
                   titlefont=dict(size=20),
                   tickfont=dict(size=15),
                   tickson='boundaries',
                   tickvals=[n for n in purch.index],
                   ticklen=10,
                   mirror=True,
                   ticks='outside',
                   type='category',
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
        margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
        showlegend=False,
        hoverlabel=dict(font=dict(size=20), namelength=-1),
    )

    fig = go.Figure(
        data=data,
        layout=layout
    )

    return fig


def plot_rel_drinks_per_person(rel_drinks_per_person):
    """Plot a bar chart to visualize who drinks what.

    Parameters
    ----------
    rel_drinks_per_person : dict
        Dictionary listing the relative amount of each drink per person.

    Returns
    -------
    fig : plotly.graph_objects.Figure
      Bar plot showing the number of each drink per person.

    """
    data = []

    for product in rel_drinks_per_person:
        drinks = rel_drinks_per_person[product].values
        person = rel_drinks_per_person[product].index

        bar = go.Bar(
            x=drinks,
            y=person,
            name=product,
            hoverinfo=('name'),
            orientation='h',
        )
        data.append(bar)

    # calculate height of plot
    height = len(person) * 50

    layout = go.Layout(
        xaxis=dict(title='Anteil an Getränken',
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
        margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
        showlegend=False,
        hoverlabel=dict(font=dict(size=20), namelength=-1),
        height=height,
        barmode='stack'
    )

    fig = go.Figure(
        data=data,
        layout=layout
    )

    return fig


def plot_abs_drinks_per_person(abs_drinks_per_person):
    """Plot a bar chart to visualize who drinks what.

    Parameters
    ----------
    abs_drinks_per_person : dict
        Dictionary listing the total number of drinks per person.

    Returns
    -------
    fig : plotly.graph_objects.Figure
      Bar plot showing the number of each drink per person.

    """
    data = [
        go.Bar(
            x=abs_drinks_per_person.values,
            y=abs_drinks_per_person.index,
            hovertemplate=('<b>%{y}</b><br>%{x} Stück<extra></extra>'),
            orientation='h',
        )
    ]

    # calculate height of plot
    height = len(abs_drinks_per_person.index) * 50

    layout = go.Layout(
        xaxis=dict(title='Anzahl an Getränken',
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
        margin={'t': 0, 'b': 0, 'l': 0, 'r': 0},
        showlegend=False,
        hoverlabel=dict(font=dict(size=20), namelength=-1),
        height=height,
    )

    fig = go.Figure(
        data=data,
        layout=layout
    )

    return fig
