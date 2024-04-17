from typing import List
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from sqlalchemy import Row


class Booking(BaseModel):
    email: EmailStr
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


class EventBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    seats: int
    name: str


def mapper_row_to_event(r: Row) -> EventBaseModel:
    if isinstance(r, Row):
        return EventBaseModel.model_validate(r[0])
    else:
        raise TypeError("Mapper row to event needs EventBaseModel")


def mapper_list_to_events(rows: List[Row]):
    return [mapper_row_to_event(r) for r in rows]
