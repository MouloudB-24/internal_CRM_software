import enum
from datetime import datetime

from sqlalchemy import Column, Integer, Datetime, ForeignKey, Enum, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Enum contract
class ContractStatus(enum.Enum):
    DRAFT = "Draft"
    PENDING = "Pending"
    SIGNED = "Signed"
    COMPLETED = "Completed"


# Contrat model
class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    sales_contact_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(ContractStatus), nullable=False, default=ContractStatus.DRAFT)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    create_at = Column(Datetime, default=datetime.now())
    update_at = Column(Datetime, default=datetime.now(), onupdate=datetime.now())

    # Relationships
    customer = relationship("Customer", back_populates="contracts")
    sales_contact = relationship("User", back_populates="managed_contracts")
    events = relationship("Event", back_populates="contract")

