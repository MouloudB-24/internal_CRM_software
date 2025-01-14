from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Initialize flask application
    app = Flask(__name__)
    app.json.sort_keys = False

    # Configure database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://aylan:aylan@localhost/crm_db'
    app.config["SECRET_KEY"] = "aylan2023"

    # Initialize SQLAlchemy with the flask application
    db.init_app(app)
    migrate.init_app(app, db)

    return app