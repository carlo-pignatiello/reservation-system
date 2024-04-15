from typing import List
from fastapi import APIRouter, Depends
from database import SessionLocal
from repos import find_all_event, book_tickets
from sqlalchemy.orm import Session
from schemas import Booking
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
def signup(session: Session = Depends(get_db)):
    events = find_all_event(session)
    return events

@order_router.post("/events/book")
def book_event(reservations_body: List[Booking], session: Session = Depends(get_db)):
    reservation = {}
    check_type_of_event = [i.event_id for i in reservations_body]
    if len(set(check_type_of_event)) != len(reservations_body):
        return {"status": "please book max three tickets for an event"}
    for book in reservations_body:
        message = book_tickets(session, book.email, book.event_id, book.ticket_no)
        reservation[book.event_id] = message
    return {"book_status": reservation}