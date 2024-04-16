from typing import List
from fastapi import APIRouter, Depends
from app.database import SessionLocal
from app.repos import find_all_event, book_tickets
from sqlalchemy.orm import Session
from app.schemas import Booking
from app.exceptions import NoDoubleEventException
# Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

order_router = APIRouter()

@order_router.get("/events/all")
def find_all(session: Session = Depends(get_db)):
    events = find_all_event(session)
    return events

@order_router.post("/events/book")
def book_event(reservations_body: List[Booking], session: Session = Depends(get_db)):
    reservation = {}
    check_type_of_event = [i.event_id for i in reservations_body]
    if len(set(check_type_of_event)) != len(reservations_body):
        raise NoDoubleEventException(message="Please book max three tickets for an event")
    for ticket in reservations_body:
        message = book_tickets(session, ticket.email, ticket.event_id, ticket.ticket_no)
        reservation[ticket.event_id] = message
    return {"book_status": reservation}