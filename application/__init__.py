from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app():
    server = Flask(__name__, instance_relative_config=False)
    server.config.from_object("config.Config")
    db.init_app(server)
    
    with server.app_context():
        # Import core parts of Flask app:
        from .models import Finance_Table
        Finance_Table.init_db()
        from . import routes
        
        # Import Dash Application: Example:
        # from .dashboard.dashboard import init_dashboard
        # server = init_dashboard(server)
        """
        For this one, I am still unsure if its "server = " or
        "app = "... Will know once I am doing this for real.
        """
        from .dashboard import init_dashapp
        server = init_dashapp(server)
        
        return server