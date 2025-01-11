import enum
from datetime import datetime

from sqlalchemy import Integer, String, Boolean, DateTime, Enum, Column
from sqlalchemy.orm import relationship

from app import db

class Departement(db.Model):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=True)
    permissions = Column(String(255), nullable=False)
    create_at = db.Column(DateTime, default=datetime.now())
    update_at = db.Column(DateTime, default=datetime.now(), onupdate=datetime.now())


    # Relation avec les utilisateurs
    users = relationship("User", back_populates="department")