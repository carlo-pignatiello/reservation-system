from sqlalchemy import and_
from models.models import Customer, Event, Reservation, CustomerSchema, EventSchema, ReservationSchema
from sqlalchemy.orm import Session
from datetime import datetime

def find_all_event(session: Session):
    e = session.query(Event).all()
    return e

def find_all_order_by_email(session: Session, email: str):
    o = session.query(Reservation).filter(Reservation.email == email).all()
    return o

def check_email(session: Session, email: str) -> int:
    customer_id = session.query(Customer).filter(Customer.email == email).first()
    if not customer_id:
        new_customer = Customer(email=email) 
        session.add(new_customer)
    customer = session.query(Customer).filter(Customer.email == email).first()
    customer = CustomerSchema.model_validate(customer)
    return customer.id

def  book_tickets(session: Session, email: str, event_id: int, tickets_no: int):
    with session.begin():
        session.connection(execution_options={"isolation_level": "SERIALIZABLE"})
        customer_id = check_email(session, email)
        event = session.query(Event).filter(and_(Event.id == event_id, Event.seats >= tickets_no)).first()
        if event:
            r = Reservation(
                seats_booked=tickets_no,
                event_id=event_id,
                customer_id=customer_id,
                expire_time=datetime.now()
            )
            session.add(r)
            event = EventSchema.model_validate(event)
            new_seats_counter = event.seats - tickets_no
            if new_seats_counter > 0:
                session.query(Event).filter(Event.id == event_id).update({Event.seats: Event.seats - tickets_no})
                return True            
            else:
                return False
# ACID quando arriva una prenotazione
# prenoto event-1 con customer_id-1 per 2 biglietti
# 1) tabella event per contrallare se ci sono almeno 2 biglietti
# 2) se ci sono (QUERY SU EVENT PER EVENTO), inserisco la riga in reservation 
# 3) UPDATE su EVENT per scalare i posti 
