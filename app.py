"""Main dash app."""
import dash
import layout

# app initialize
app = dash.Dash(
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
)

# layout
app.layout = layout.serve_layout()
