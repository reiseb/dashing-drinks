"""Main dash app."""
import callbacks
import dash
import flask
import layout
from dotenv import load_dotenv

# flask server for production environment
server = flask.Flask(__name__)

# load environment variables
load_dotenv()

# app initialize
dashapp = dash.Dash(
    __name__,
    external_stylesheets=[
        "assets/css/bootstrap.css",
        "assets/css/fontawesome.css"
    ],
    # these meta_tags ensure content is scaled correctly on different devices
    # see: https://www.w3schools.com/css/css_rwd_viewport.asp for more
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1"
        }
    ],
    url_base_pathname='/getraenke/',
    server=server
)

# register layout
dashapp.layout = layout.serve_layout()

# register callbacks
callbacks.register_callbacks(dashapp)
