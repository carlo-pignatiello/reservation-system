from typing import List
from fastapi import APIRouter, Depends
from app.database import get_session
from app.repos import find_all_event, book_tickets
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import Booking
from app.exceptions import NoDoubleEventException
# Base.metadata.create_all(bind=engine)


# Dependency
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


order_router = APIRouter()


@order_router.get("/events/all")
async def find_all(session: AsyncSession = Depends(get_session)):
    events = await find_all_event(session)
    return events


@order_router.post("/events/book")
async def book_event(
    reservations_body: List[Booking], session: AsyncSession = Depends(get_session)
):
    reservation = {}
    check_type_of_event = [i.event_id for i in reservations_body]
    if len(set(check_type_of_event)) != len(reservations_body):
        raise NoDoubleEventException(
            message="Please book max three tickets for an event"
        )
    for ticket in reservations_body:
        tickets, reservation_id, event_name = await book_tickets(
            session, ticket.email, ticket.event_id, ticket.ticket_no
        )
        reservation[event_name] = {
            "email": ticket.email,
            "tickets_seats": tickets,
            "order_no": reservation_id,
        }
    return reservation
