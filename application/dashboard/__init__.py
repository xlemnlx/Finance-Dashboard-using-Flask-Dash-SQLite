from .layout import init_layout
from .callbacks import init_callbacks
from dash import Dash

def init_dashapp(server):
    
    """Create a Plotly Dash dashboard."""
    app = Dash(server=server,
               routes_pathname_prefix="/dashboard/",
               external_stylesheets=["../static/css/styles.css"],)
    
    # Initialize Dash Layout.
    init_layout(app)
    
    # Initialize callbacks after the app is loaded.
    init_callbacks(app)
    
    return app.server
    