import enum
from datetime import datetime

from sqlalchemy import Column, Integer, Datetime, ForeignKey, Enum, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Enum event
class EventStatus(enum.Enum):
    PLANNED = "Planned"
    IN_PROGRESS = "In progress"
    COMPLETED = "Completed"


# Even class
class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    support_contact_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String(100), nullable=False)
    status = Column(Enum(EventStatus), default=EventStatus.PLANNED)
    start_date = Column(Datetime, nullable=False)
    end_date = Column(Datetime, nullable=False)
    location = Column(String(150), nullable=False)
    attendees = Column(Integer)
    notes = Column(String(1000))
    create_at = Column(Datetime, default=datetime.now())
    update_at = Column(Datetime, default=datetime.now(), onupdate=datetime.now())


    # Relations
    contract = relationship("Contract", back_populates="events")
    support_contact = relationship("User", back_populates="supported_events")