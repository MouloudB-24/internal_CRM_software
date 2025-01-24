import enum
from datetime import datetime, timedelta

import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from app.models.customer import Customer


# Define a role class
class UserRole(enum.Enum):
    SALES = "Sales"
    SUPPORT = "Support"
    MANAGEMENT = "Management"


# Define a User model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    create_at = db.Column(db.DateTime, default=db.func.now())
    update_at = db.Column(db.DateTime, default=db.func.now(), onupdate=datetime.now())
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    managed_customers = db.relationship("Customer", back_populates="sales_contact")
    managed_contracts = db.relationship("Contract", back_populates="sales_contact")
    supported_events = db.relationship("Event", back_populates="support_contact")


    def __repr__(self):
        return f"User {self.username}"

    def set_password(self, password):
        """Hash password"""
        self.password = generate_password_hash(password)


    def check_password(self, password):
        """Check hashed password"""
        return check_password_hash(self.password, password)


    def generate_token(self, expiration=10800):
        """Gererate a JWT for user with an expiration date"""

        payload = {"user_id": self.id, "exp": datetime.now() + timedelta(seconds=expiration)}

        token = jwt.encode(payload, key=current_app.config["SECRET_KEY"], algorithm="HS256")
        return token

    @staticmethod
    def verify_token(token):
        """Check a JWT and returns the user ID if valid"""

        try:
            payload = jwt.decode(token, key=current_app.config["SECRET_KEY"], algorithms=["HS256"])
            return payload['user_id']

        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None