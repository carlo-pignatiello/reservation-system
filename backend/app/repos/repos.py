import random
import time
from typing import List, Tuple
from sqlalchemy import select, update, and_
from app.models import Customer, Event, Reservation
from app.schemas import CustomerSchema, EventSchema, EventBaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.logger import logger
from app.exceptions import (
    NoCustomerExistanceException,
    NoEventException,
    TicketNotAvailableException,
)
from app.schemas.schemas import ReservationSchema, mapper_list_to_events


async def find_all_event(session: AsyncSession) -> List[EventBaseModel]:
    """Retrieves all event data from the database.

    This function executes a query to fetch all rows from the `Event` table.
    It raises a `NoEventException` if no events are found.
    It then maps the raw results to `EventBaseModel` instances and returns them.

    Args:
        session (AsyncSession): An asynchronous database session dependency.

    Raises:
        NoEventException: If no events are found in the database.

    Returns:
        List[EventBaseModel]: A list of `EventBaseModel` objects representing all events.
    """
    res = await session.execute(select(Event))
    events = res.fetchall()
    if not events:
        raise NoEventException(message="No event with this name")
    return mapper_list_to_events(list(events))


async def check_email(session: AsyncSession, email: str) -> int:
    """Retrieves the customer ID associated with an email address.

    This function searches for a customer in the `Customer` table
    based on the provided email address. It raises a `NoCustomerExistanceException`
    if no customer is found. It then validates the retrieved customer data
    using `CustomerSchema.model_validate` and returns the customer ID.


    Args:
        session (AsyncSession): An asynchronous database session dependency.
        email (str): The email address to search for.

    Raises:
        NoCustomerExistanceException: If no customer with the given email exists.

    Returns:
        int:  The ID of the customer associated with the email.
    """
    res = await session.execute(select(Customer).where(Customer.email == email))
    customer = res.first()
    if not customer:
        raise NoCustomerExistanceException(message="No customer with this email")
    customer = CustomerSchema.model_validate(customer[0])
    return customer.id


async def get_event(session: AsyncSession, event_id: int) -> EventSchema:
    """
    Args:
        session (AsyncSession): An asynchronous database session dependency.
        event_id (int): The ID of the event to retrieve.

    Raises:
        NoEventException: If no event with the given ID is found.

    Returns:
        EventSchema: An `EventSchema` object representing the retrieved event details.
    """
    res = await session.execute(select(Event).where(Event.id == event_id))
    event = res.first()
    if not event:
        raise NoEventException(message="No event with this name")
    event = EventSchema.model_validate(event[0])
    return event


# @retry(times=3, exceptions=TicketNotAvailableError)
async def book_tickets(
    session: AsyncSession, email: str, event_id: int, tickets_no: int
) -> Tuple[list, int, str]:
    """Books tickets for an event if available, creating a reservation.

    This function attempts to book the specified number of tickets for an event
    using optimistic locking. It performs the following steps:

    1. Retrieves the customer ID associated with the email.
    2. Fetches event details based on the event ID.
    3. Calls `booking_transaction` to handle the optimistic locking logic
       and reservation creation.
    4. Returns a tuple containing:
        - A list of booked seat numbers (1-based indexing).
        - The ID of the created reservation (if successful).
        - The name of the booked event.

    Args:
        session (AsyncSession): An asynchronous database session dependency.
        email (str): The email address of the customer booking tickets.
        event_id (int): The ID of the event for which tickets are being booked.
        tickets_no (int): The number of tickets to be booked.

    Returns:
        Tuple[list, int, str]: A tuple containing the booked seat numbers, reservation ID, and event name.
    """
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
    """Attempts to book a specified number of tickets for an event.

    This function implements optimistic locking to handle potential race conditions
    during concurrent booking attempts. It tries to update the event's available
    seats and create a reservation if enough seats are available.

    Args:
        session (AsyncSession): An asynchronous database session dependency.
        event (EventSchema): An instance of the `EventSchema` representing the event.
        tickets_no (int): The number of tickets to be booked.
        customer_id (int): The ID of the customer making the booking.

    Raises:
        TicketNotAvailableException: If insufficient seats are available or
        another transaction booked them first.
    Returns:
        Tuple[list, int]:
            - A list of booked seat numbers (1-based indexing).
            - The ID of the created reservation (if successful).
    """
    current_version = event.version
    # Optimistic locking with update statement
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
    # Retry logic with exponential backoff for potential conflicts
    attemp = 0
    while attemp < 5:
        res = await session.execute(stmt)
        rowcount = res.rowcount
        if not rowcount:
            logger.info(f"Counter {attemp}")
            attemp += 1
            delay = 0.001 * (2**attemp + random.uniform(0, 1))
            logger.info(f"Sleeping for {delay}s...")
            time.sleep(delay)
            continue
        r = Reservation(
            seats_booked=tickets_no, event_id=event.id, customer_id=customer_id
        )
        session.add(r)
        await session.flush()
        await session.refresh(r)
        # Successful update (enough seats available)
        reservation = ReservationSchema.model_validate(r)
        return list(
            range(event.seats - tickets_no + 1, event.seats + 1)
        ), reservation.id
    else:
        # Update failed (seats unavailable)
        raise TicketNotAvailableException(
            message="Ticket already booked", event_id=event.id
        )

    # except TicketNotAvailableError as e:  # sqlalchemy.exc.OperationalError
    #     await session.rollback()
    #     raise TicketNotAvailableException(message="Ticket already booked")
