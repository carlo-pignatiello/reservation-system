from typing import Tuple
import sqlalchemy
from app.models import Customer, Event, Reservation
from app.schemas import CustomerSchema, EventSchema
from sqlalchemy.orm import Session
from app.logger import logger
from app.utils import retry
from app.exceptions import (
    NoCustomerExistanceException,
    NoEventException,
    TicketNotAvailableException,
)
from app.schemas.schemas import ReservationSchema


def find_all_event(session: Session):
    e = session.query(Event).all()
    return e


def check_email(session: Session, email: str) -> int:
    customer_id = session.query(Customer).filter(Customer.email == email).first()
    if not customer_id:
        raise NoCustomerExistanceException(message="No customer with this email")
    customer = session.query(Customer).filter(Customer.email == email).first()
    customer = CustomerSchema.model_validate(customer)
    return customer.id


def get_event(session: Session, event_id: int) -> EventSchema:
    event = session.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise NoEventException(message="No event with this name")
    event = EventSchema.model_validate(event)
    return event


@retry(
    times=3, exceptions=(sqlalchemy.exc.OperationalError, TicketNotAvailableException)
)
def book_tickets(
    session: Session, email: str, event_id: int, tickets_no: int
) -> Tuple[list, int, str]:
    with session.begin():
        session.connection(execution_options={"isolation_level": "SERIALIZABLE"})
        customer_id = check_email(session, email)
        event = get_event(session, event_id)
        tickets_booked, reservation_id = booking_transaction(
            session, event, tickets_no, customer_id
        )
        return tickets_booked, reservation_id, event.name


def booking_transaction(
    session: Session, event: EventSchema, tickets_no: int, customer_id: int
) -> Tuple[list, int]:
    try:
        r = Reservation(
            seats_booked=tickets_no, event_id=event.id, customer_id=customer_id
        )
        session.add(r)
        session.flush()
        session.refresh(r)
        reservation = ReservationSchema.model_validate(r)
        new_seats_counter = event.seats - tickets_no
        if new_seats_counter > 0:
            session.query(Event).filter(Event.id == event.id).update(
                {Event.seats: Event.seats - tickets_no}
            )
            return list(range(new_seats_counter + 1, event.seats + 1)), reservation.id
        else:
            raise TicketNotAvailableException(message="Ticket not available")
    except sqlalchemy.exc.OperationalError as e:
        logger.error("Ticket already booked")
        session.rollback()
        raise e
