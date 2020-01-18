"""Build the layout of the dashboard."""
import dash_bootstrap_components as dbc
import dash_html_components as html


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
            html.H1(
                children=('Getränkekasse'),
                className='display-4',
                style={
                    'margin-top': '4rem',
                    'margin-bottom': '3rem'
                }
            ),
            html.P(
                dbc.Row(
                    dbc.Col(
                        build_info_cards(),
                        width=12
                    )
                )
            )
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
                ident="info-box-favorite",
                icon="fa fa-heart",
                title="Kassenschlager",
                value="Bionade",
                color="#802020"
            ),
            info_card(
                ident="info-box-royal",
                icon="fa fa-crown",
                title="Getränkekönig*in",
                value="user",
                color="#a07000"
            ),
            info_card(
                ident="info-box-money",
                icon="fa fa-money-bill-wave",
                title="Umsatz",
                value="0 €",
                color="#216b27"
            ),
        ]
    )
    return cards


def info_card(ident, icon, title, value, color):
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
                            html.I(
                                className=icon,
                                style={
                                    'padding-top': '10%',
                                    'font-size': '500%',
                                    'color': '#eeeeee',
                                    'opacity': '0.5',
                                    'vertical-align': 'middle'
                                }
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            children=[
                                html.H1(
                                    id=ident + "-value",
                                    children=value,
                                    style={
                                        'font-weight': 'bold',
                                        'font-size': '300%',
                                        'color': '#eeeeee'
                                    }
                                ),
                                html.H5(
                                    id=ident + "-title",
                                    children=title,
                                    style={
                                        'color': '#eeeeee',
                                    }
                                )
                            ],
                            width=7
                        )
                    ]
                )
            ]
        ),
        style={'background-color': color}
    )
    return card
