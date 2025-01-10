import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, Datetime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Definition enums
class UserRole(enum.Enum):
    SALES = "Sales"
    SUPPORT = "Support"
    MANAGEMENT = "Management"

# User model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    create_at = Column(Datetime, default=datetime.now())
    update_at = Column(Datetime, default=datetime.now(), onupdate=datetime.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    managed_customers = relationship("Customer", back_populates="sales_contact")
    managed_contracts = relationship("Contrat", back_populates="sales_contact")
    events = relationship("Event", back_populates="support_contact")
