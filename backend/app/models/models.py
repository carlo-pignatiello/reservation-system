from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from database import Base
from pydantic import BaseModel, ConfigDict

class Event(Base):
    """Event model"""

    __tablename__ = "event"
    id = Column(Integer, primary_key=True)
    seats = Column(Integer)
    name = Column(String)


class Customer(Base):
    """Customer model"""

    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)


class Reservation(Base):
    """Reservation model"""

    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True)
    seats_booked = Column(Integer)
    event_id = Column(Integer, ForeignKey("event.id"))
    customer_id = Column(String, ForeignKey("customer.id"))
    expire_time = Column(DateTime, default=datetime.now())


class EventSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    seats: int
    name: str

class CustomerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: str

class ReservationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    seats_booked: int
    event_id: int
    customer_id: int
    expire_time: datetime