import enum
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from app import db


# Definition enums
class UserRole(enum.Enum):
    SALES = "Sales"
    SUPPORT = "Support"
    MANAGEMENT = "Management"

# User model
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    department_id = db.Column(Integer, ForeignKey("departments.id"), nullable=False)
    username = db.Column(String(50), unique=True, nullable=False)
    password = db.Column(String(255), nullable=False)
    email = db.Column(String(100), unique=True, nullable=False)
    phone = db.Column(String(20), nullable=False)
    create_at = db.Column(DateTime, default=datetime.now())
    update_at = db.Column(DateTime, default=datetime.now(), onupdate=datetime.now())
    is_active = db.Column(Boolean, default=True)

    # Relationships
    managed_customers = relationship("Customer", back_populates="sales_contact")
    managed_contracts = relationship("Contrat", back_populates="sales_contact")
    supported_events = relationship("Event", back_populates="support_contact")
    department = relationship("Department", back_populates="users")


    def set_password(self, password):
        """Hash le mot de passe"""
        self.password = generate_password_hash(password)


    def check_password(self, password):
        """Verifier le mot de passe haché"""
        return check_password_hash(self.password, password)
