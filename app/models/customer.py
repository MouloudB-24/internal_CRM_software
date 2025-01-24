from datetime import datetime

from app import db
from app.models.contract import Contract


# Customer model
class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    sales_contact_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company_name = db.Column(db.String(100), nullable=True)
    last_contact_date = db.Column(db.DateTime, default=datetime.now())


    # Relationships
    sales_contact = db.relationship("User", back_populates="managed_customers")
    contracts = db.relationship("Contract", back_populates="customer")
