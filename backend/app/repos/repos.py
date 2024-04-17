from typing import List, Tuple
from sqlalchemy import select, update, and_
from app.models import Customer, Event, Reservation
from app.schemas import CustomerSchema, EventSchema, EventBaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.logger import logger
from app.utils import retry
from app.exceptions import (
    NoCustomerExistanceException,
    NoEventException,
    TicketNotAvailableException,
)
from app.schemas.schemas import ReservationSchema, mapper_list_to_events


async def find_all_event(session: AsyncSession) -> List[EventBaseModel]:
    res = await session.execute(select(Event))
    events = res.fetchall()
    if not events:
        raise NoEventException(message="No event with this name")
    return mapper_list_to_events(list(events))


async def check_email(session: AsyncSession, email: str) -> int:
    res = await session.execute(select(Customer).where(Customer.email == email))
    customer = res.first()
    if not customer:
        raise NoCustomerExistanceException(message="No customer with this email")
    customer = CustomerSchema.model_validate(customer[0])
    return customer.id


async def get_event(session: AsyncSession, event_id: int) -> EventSchema:
    res = await session.execute(select(Event).where(Event.id == event_id))
    event = res.first()
    if not event:
        raise NoEventException(message="No event with this name")
    event = EventSchema.model_validate(event[0])
    return event


@retry(times=3, exceptions=(Exception, TicketNotAvailableException))
async def book_tickets(
    session: AsyncSession, email: str, event_id: int, tickets_no: int
) -> Tuple[list, int, str]:
    async with session.begin():
        # await session.connection(execution_options={"isolation_level": "SERIALIZABLE"})
        customer_id = await check_email(session, email)
        event = await get_event(session, event_id)
        tickets_booked, reservation_id = await booking_transaction(
            session, event, tickets_no, customer_id
        )
        return tickets_booked, reservation_id, event.name


async def booking_transaction(
    session: AsyncSession, event: EventSchema, tickets_no: int, customer_id: int
) -> Tuple[list, int]:
    try:
        current_version = event.version
        stmt = (
            update(Event)
            .where(
                and_(
                    Event.id == event.id,
                    Event.version == current_version,
                    Event.seats >= tickets_no,
                )
            )
            .values(
                {
                    Event.seats: Event.seats - tickets_no,
                    Event.version: Event.version + 1,
                }
            )
        )
        res = await session.execute(stmt)
        rowcount = res.rowcount
        logger.info(f"{rowcount}")
        if not rowcount:
            raise TicketNotAvailableException(message="Ticket not available")
        r = Reservation(
            seats_booked=tickets_no, event_id=event.id, customer_id=customer_id
        )
        session.add(r)
        await session.flush()
        await session.refresh(r)
        reservation = ReservationSchema.model_validate(r)
        return list(
            range(event.seats - tickets_no + 1, event.seats + 1)
        ), reservation.id

    except Exception as e:  # sqlalchemy.exc.OperationalError
        logger.error("Ticket already booked")
        await session.rollback()
        raise e
