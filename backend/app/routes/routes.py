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
    """Retrieves all events from the database.

    This function is an asynchronous handler for the `/events/all` endpoint.
    It injects an AsyncSession dependency using `Depends(get_session)`.
    It then fetches all events using `find_all_event(session)` and returns them.
    """
    events = await find_all_event(session)
    return events


@order_router.post("/events/book")
async def book_event(
    reservations_body: Booking, session: AsyncSession = Depends(get_session)
):
    """Books tickets for multiple events specified in the request body.

    This function is an asynchronous handler for the `/events/book` endpoint.
    It takes a list of `Booking` objects representing the event bookings.
    It raises `NoDoubleEventException` if a booking attempts to reserve
    more than one ticket for the same event.

    Args:
        reservations_body: A list of `Booking` objects containing booking details.
        session: An asynchronous database session dependency (injected).

    Returns:
        A dictionary mapping event names to their corresponding booking details,
        including email, reserved tickets, and order number.
    """
    orders = reservations_body.ticket
    check_type_of_event = [i.event_id for i in orders]
    if len(set(check_type_of_event)) != len(orders):
        raise NoDoubleEventException(
            message="Please book book one event for transaction"
        )
    for ticket in orders:
        tickets, reservation_id, event_name = await book_tickets(
            session, reservations_body.email, ticket.event_id, ticket.ticket_no
        )
    return {
        "email": reservations_body.email,
        event_name: {
            "tickets_seats": tickets,
            "order_no": reservation_id,
        },
    }
