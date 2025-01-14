import enum
from datetime import datetime

from sqlalchemy import Integer, DateTime, ForeignKey, Enum, String
from sqlalchemy.orm import relationship

from app import db


# Enum event
class EventStatus(enum.Enum):
    PLANNED = "Planned"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


# Even class
class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(Integer, primary_key=True, autoincrement=True)
    contract_id = db.Column(Integer, ForeignKey("contracts.id"))
    support_contact_id = db.Column(Integer, ForeignKey("users.id"))
    name = db.Column(String(100), nullable=False)
    status = db.Column(Enum(EventStatus), default=EventStatus.PLANNED)
    start_date = db.Column(DateTime, nullable=False)
    end_date = db.Column(DateTime, nullable=False)
    location = db.Column(String(150), nullable=False)
    attendees = db.Column(Integer)
    notes = db.Column(String(1000))
    create_at = db.Column(DateTime, default=datetime.now())
    update_at = db.Column(DateTime, default=datetime.now(), onupdate=datetime.now())


    # Relations
    contract = relationship("Contract", back_populates="events")
    support_contact = relationship("User", back_populates="supported_events")