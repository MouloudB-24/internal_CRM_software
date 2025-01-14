import enum
from datetime import datetime

from app import db


# Define a Status class
class ContractStatus(enum.Enum):
    DRAFT = "Draft"
    PENDING = "Pending"
    SIGNED = "Signed"
    COMPLETED = "Completed"


# Define Contract model
class Contract(db.Model):
    __tablename__ = "contracts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"), nullable=False)
    sales_contact_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.Enum(ContractStatus), nullable=False, default=ContractStatus.DRAFT)
    total_amount = db.Column(db.Float, nullable=False)
    remaining_amount = db.Column(db.Float, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now())
    update_at = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

    # Relationships
    customer = db.relationship("Customer", back_populates="contracts")
    sales_contact = db.relationship("User", back_populates="managed_contracts")
    events = db.relationship("Event", back_populates="contract")

