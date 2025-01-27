import os

import sentry_sdk
from flask import Flask
from flask.cli import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sentry_sdk.integrations.logging import LoggingIntegration

# Load environment variables from .env file
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


# Initialize Sentry
sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[LoggingIntegration()],
    traces_sample_rate=1.0,
    _experiments={"continuous_profiling_auto_start": True}
)


def create_app():
    # Initialize flask application
    app = Flask(__name__)
    app.json.sort_keys = False

    # Import all models
    from app.models.user import User
    from app.models.customer import Customer
    from app.models.contract import Contract
    from app.models.event import Event

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