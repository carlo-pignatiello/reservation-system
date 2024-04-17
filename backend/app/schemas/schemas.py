from typing import List
from pydantic import BaseModel, Field, ConfigDict


class Booking(BaseModel):
    email: str
    event_id: int
    ticket_no: int = Field(gt=0, le=3)


class EventSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    seats: int
    name: str
    version: int


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


class Ticket(BaseModel):
    email: str
    ticket_no: List[int]
    reservation_order: int


# def map_to_event(d: Event) -> EventSchema:
#     print(d.as)
#     return EventSchema.model_validate(d.as)

# def map_to_events(events: list) -> List[EventSchema]:
#     return [map_to_event(i) for i in events]
