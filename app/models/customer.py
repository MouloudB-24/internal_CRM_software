from datetime import datetime

from sqlalchemy import Column, Integer, String, Datetime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# Customer model
class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sales_contract_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    company_name = Column(String(100), nullable=True)
    last_contact_date = Column(Datetime, default=datetime.now())


    # Relationships
    sales_contract = relationship("User", back_populates="managed_customers")
    contracts = relationship("Contrat", back_populates="customer")
