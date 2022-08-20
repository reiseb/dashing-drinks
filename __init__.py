"""Initialize the app in a larger flask application."""
import dash

from dotenv import load_dotenv
from .layout import serve_layout
from .callbacks import register_callbacks


def create_app(server):
    """Create the app."""
    load_dotenv()

    # Meta tags for viewport responsiveness
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no"
    }

    # CSS
    external_stylesheets = ['/static/bootstrap.css',
                            '/static/style.css',
                            '/static/navbar.css']

    # JavaScript for the navigation bar
    external_scripts = [
        {"src": "https://code.jquery.com/jquery-3.4.1.slim.min.js",
         "integrity": "sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n", # noqa
         "crossorigin": "anonymous"
         },
        {"src": "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js", # noqa
         "integrity": "sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6", # noqa
         "crossorigin": "anonymous"
         }
    ]

    # Dashboard app
    dashapp = dash.Dash(__name__,
                        server=server,
                        url_base_pathname='/getraenke/',
                        external_stylesheets=external_stylesheets,
                        external_scripts=external_scripts,
                        meta_tags=[meta_viewport]
                        )

    with server.app_context():
        dashapp.title = 'Getraenkekasse - AK de Vivie-Riedle'
        dashapp.layout = serve_layout()
        register_callbacks(dashapp)

    return dashapp
