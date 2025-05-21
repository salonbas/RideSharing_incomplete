# === dao/event_dao.py ===
from models.models import Event
from config.db import get_session

def get_all_events():
    session = get_session()
    return session.query(Event).all()

def get_event_by_id(event_id):
    session = get_session()
    return session.query(Event).filter_by(id=event_id).first()

def update_event(event):
    session = get_session()
    session.add(event)
    session.commit()
