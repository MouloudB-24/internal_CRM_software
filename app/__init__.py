import os

from flask import Flask
from flask.cli import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Initialize flask application
    app = Flask(__name__)
    app.json.sort_keys = False

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] =  os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')

    if not app.config['SQLALCHEMY_DATABASE_URI']:
        raise ValueError("Missing SQLALCHEMY_DATABASE_URI in environment variables")

    if not app.config['SECRET_KEY']:
        raise ValueError("Missing SECRET_KEY in environment variables")

    # Initialize SQLAlchemy with the flask application
    db.init_app(app)
    migrate.init_app(app, db)

    return app