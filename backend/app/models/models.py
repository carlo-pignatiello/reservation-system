from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base

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
    customer_id = Column(Integer, ForeignKey("customer.id"))
