import enum
from datetime import datetime

from werkzeug.security import generate_password_hash

from app import db


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

    def set_password(self, password):
        """Hash password"""
        self.password = generate_password_hash(password)

