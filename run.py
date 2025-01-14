from app import create_app, db
from app.models.user import User
from app.models.customer import Customer
from app.models.contract import Contract
from app.models.event import Event

app = create_app()

from app.controllers.user_controller import user_bp
app.register_blueprint(user_bp, url_prefix='/users')

from app.controllers.data_controller import data_bp
app.register_blueprint(data_bp, url_prefix="/data")

from app.controllers.customer_controller import customer_bp
app.register_blueprint(customer_bp, url_prefix="/customers")

from app.controllers.contract_controller import contract_bp
app.register_blueprint(contract_bp, url_prefix="/contracts")

from app.controllers.event_controller import event_bp
app.register_blueprint(event_bp, url_prefix="/events")

# Crée les tables avant de lancer l'application
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)