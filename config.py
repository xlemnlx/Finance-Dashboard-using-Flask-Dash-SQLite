"""Flask configs."""

from os import environ, path

BASE_DIR = path.abspath(path.dirname(__file__))
db_path = path.join(BASE_DIR, "application", "static", "db", "finance.db")

class Config:
    """Flask configuration variables:"""
    
    # General config:
    ENVIRONMENT = environ.get("ENVIRONMENT")
    FLASK_APP = "main.py"
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")
    
    # Static assets:
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{db_path}"