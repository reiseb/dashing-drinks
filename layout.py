"""Build the layout of the dashboard."""
import dash_bootstrap_components as dbc
import dash_html_components as html


def serve_layout():
    """Build the top-level dashboard layout.

    Contains two hidden divs with the number of the currently selected
    state and the colormap sharedSacross callbacks.

    Returns
    -------
    layout : dash_html_components.Div
        HTML Layout for the dashboard.

    """
    layout = dbc.Container(
        style={'max-width': '95%'},
        children=[
            # title
            html.H1(
                children=('Getränkekasse'),
                className='display-4',
                style={'margin-top': '4rem',
                       'margin-bottom': '3rem'}
            ),
        ],
    )
    return layout
