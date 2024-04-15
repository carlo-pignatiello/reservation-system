from typing import Optional
import sqlalchemy
from models import Customer, Event, Reservation
from schemas import CustomerSchema, EventSchema
from sqlalchemy.orm import Session
from logger import logger
from exceptions import NoEventError
from utils import retry

def find_all_event(session: Session):
    e = session.query(Event).all()
    return e

def check_email(session: Session, email: str) -> int:
    customer_id = session.query(Customer).filter(Customer.email == email).first()
    if not customer_id:
        new_customer = Customer(email=email) 
        session.add(new_customer)
    customer = session.query(Customer).filter(Customer.email == email).first()
    customer = CustomerSchema.model_validate(customer)
    return customer.id

def get_event(session: Session, event_id: int) -> Optional[EventSchema]:
    event = session.query(Event).filter(Event.id == event_id).first()
    if not event:
        return None
    event = EventSchema.model_validate(event)
    return event

@retry(times=3, exceptions=(sqlalchemy.exc.OperationalError))
def book_tickets(session: Session, email: str, event_id: int, tickets_no: int) -> Optional[list]:
    with session.begin():
        session.connection(execution_options={"isolation_level": "SERIALIZABLE"})
        customer_id = check_email(session, email)
        event = get_event(session, event_id)
        if event:
            tickets_booked = booking_transaction(session, event, tickets_no, customer_id)
            return tickets_booked
        raise NoEventError()

def booking_transaction(session: Session, event: EventSchema, tickets_no: int, customer_id: int) -> Optional[list]:
    try:
        r = Reservation(
            seats_booked=tickets_no,
            event_id=event.id,
            customer_id=customer_id
        )
        session.add(r)
        new_seats_counter = event.seats - tickets_no
        if new_seats_counter > 0:
            session.query(Event).filter(Event.id == event.id).update({Event.seats: Event.seats - tickets_no})
            return list(range(new_seats_counter, event.seats))
    except sqlalchemy.exc.OperationalError as e:
        logger.error("Ticket already booked")
        session.rollback()
        raise e