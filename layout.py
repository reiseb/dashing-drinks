"""Build the layout of the dashboard."""
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash_table.Format import Format


def serve_layout():
    """Build the top-level dashboard layout.

    Contains two hidden divs with the number of the currently selected
    state and the colormap sharedSacross callbacks.

    Returns
    -------
    layout : dash_bootstrap_components.Container
        Bootstrap container with the top-level layout.

    """
    layout = dbc.Container(
        style={'max-width': '80%'},
        children=[
            # update every 15 minutes
            dcc.Interval(
                id='interval-component',
                interval=15 * 60 * 1000,  # in milliseconds
                n_intervals=0
            ),
            # hidden div for shared data
            html.Div(
                id='shared_data',
                children=[],
                style={'display': 'none'}
            ),
            # title
            html.H1(
                children=('Getränkekasse'),
                className='display-5',
                style={
                    'margin-top': '3rem',
                    'margin-bottom': '3rem'
                }
            ),
            # info boxes
            html.P(
                dbc.Row(
                    children=[
                        dbc.Col(
                            build_info_cards(),
                            width=12
                        )
                    ]
                )
            ),
            html.P(
                dbc.Row(
                    children=[
                        dbc.Col(
                            build_timeline(),
                            width=12
                        )
                    ]
                )
            ),
            # content
            html.P(
                dbc.CardDeck(
                    children=[
                        build_inventory_overview(),
                        build_chart(),
                        build_debt_table(),
                    ]
                )
            ),
        ],
    )
    return layout


def build_info_cards():
    """Build the top row of the layout with info cards.

    Returns
    -------
    cards : dash_bootstrap_components.CardDeck
        CardDeck with info cards. CardDeck takes care that all
        cards are the same height and width.

    """
    cards = dbc.CardDeck(
        children=[
            info_card(
                ident="info-box-bestseller",
                icon="fa fa-heart",
                title="Bestseller des Monats",
                value="",
                color="#802020",
                fontsize="300%"
            ),
            info_card(
                ident="info-box-royal",
                icon="fa fa-crown",
                title="Getränkekönig*in",
                value="",
                color="#a07000",
                fontsize="300%"
            ),
            info_card(
                ident="info-box-revenue",
                icon="fa fa-money-bill-wave",
                title="",
                value="",
                color="#216b27",
                fontsize="300%"
            ),
        ]
    )
    return cards


def info_card(ident, icon, title, value, color, fontsize):
    """Build a single info card.

    Parameters
    ----------
    ident : str
        ID basename of the layout element. Will be used to
        generate IDs for title and value of the info box.
    icon : str
        FontAwesome icon name.
    title : str
        Title of the info card. Accessible in callbacks via <ident>-title.
    value : str
        Value of the info card. Accessible in callbacks via <ident>-value.
    color : str
        Background color in hex notation (e.g. '#000000')
    fontsize : str
        CSS fontsize property.

    Returns
    -------
    card : dash_bootstrap_components.Card
        Info card layout element.

    """
    card = dbc.Card(
        dbc.CardBody(
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                html.H1(
                                    id=ident + "-value",
                                    children=value,
                                    style={
                                        'font-weight': 'bold',
                                        'font-size': fontsize,
                                        'color': '#eeeeee'
                                    }
                                ),
                                html.H5(
                                    id=ident + "-title",
                                    children=title,
                                    style={
                                        'color': '#eeeeee',
                                        'margin-bottom': '0pt',
                                    }
                                )
                            ],
                            width=9,
                        ),
                        dbc.Col(
                            html.I(
                                className=icon,
                                style={
                                    'font-size': '450%',
                                    'color': '#eeeeee',
                                    'opacity': '0.5',
                                    'text-align': 'center'
                                }
                            ),
                            width=3,
                        ),
                    ],
                )
            ],
        ),
        style={'background-color': color}
    )
    return card


def build_timeline():
    """Build a timeline.

    Returns
    -------
    card : dash_bootstrap_components.Card
        Card with a dcc.Graph element.

    """
    card = dbc.Card(
        children=[
            dbc.CardHeader(
                html.H2("Käufe über Zeit"),
            ),
            dbc.CardBody(
                children=[
                    dcc.Graph(
                        id="timeline",
                        figure={},
                    ),
                ]
            )
        ]
    )
    return card


def build_debt_table():
    """Build a table with current debts."""
    card = dbc.Card(
        children=[
            dbc.CardHeader(
                children=[
                    html.H2("Ausstehende Zahlungen"),
                ]
            ),
            dbc.CardBody(
                dash_table.DataTable(
                    id='debt_table',
                    columns=[
                        {
                            'id': 'name',
                            'name': 'Name',
                            'type': 'text'
                        }, {
                            'id': 'price',
                            'name': 'Schulden [EUR]',
                            'type': 'numeric',
                            'format': Format(
                                scheme='f',
                                precision=2
                            ),
                        }
                    ],
                    data=[],
                    style_table={
                        'maxHeight': '835px',
                    },
                    style_header={
                        'backgroundColor': '#d1d1d1ff',
                        'fontWeight': 'bold',
                        'fontSize': '130%',
                        'textAlign': 'center',
                    },
                    style_cell={
                        'padding': '5px',
                        'textAlign': 'center',
                        'fontSize': '120%',
                        'fontFamily': 'Helvetica',
                        'height': '120%'
                    },
                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': '#f5f5f5ff'
                        }
                    ],
                    style_as_list_view=True,
                    filter_action="none",
                    sort_action="native",
                )
            )
        ]
    )
    return card


def build_inventory_overview():
    """Build an inventory summary."""
    card = dbc.Card(
        children=[
            dbc.CardHeader(
                html.H2("Inventar"),
            ),
            dbc.CardBody(
                children=[
                    dcc.Graph(
                        id="inventory",
                        figure={},
                    ),
                ]
            )
        ]
    )
    return card


def build_chart():
    """Build a diagram of who purchased what."""
    card = dbc.Card(
        children=[
            dbc.CardHeader(
                html.H2("Statistik"),
            ),
            dbc.CardBody(
                children=[
                    dcc.Graph()
                ]
            )
        ]
    )
    return card
