from pydantic import BaseModel, Field

class Booking(BaseModel):
    email: str
    event_id: int
    ticket_no: int = Field(gt=0, le=3)

# def map_to_event(d: Event) -> EventSchema:
#     print(d.as)
#     return EventSchema.model_validate(d.as)

# def map_to_events(events: list) -> List[EventSchema]:
#     return [map_to_event(i) for i in events]
