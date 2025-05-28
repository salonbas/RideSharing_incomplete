# === dao/event_dao.py ===
from models.models import Event
from config.db import get_session
from datetime import datetime

def get_all_events():
    session = get_session()
    return session.query(Event).all()

def get_event_by_id(event_id):
    session = get_session()
    return session.query(Event).filter_by(id=event_id).first()

def create_event(event_data):  # 新增這個方法
    session = get_session()
    
    print("DEBUG: Entered create_event")
    print("DATA: event_data =", event_data)
    try:
        new_event = Event(
            title=event_data['title'],
            description=event_data['description'],
            type=event_data['type'],
            date=datetime.fromisoformat(event_data['date']),
            requiredSeats=int(event_data['requiredSeats']),
            joinedSeats=0,
            organizer_id=int(event_data['organizer_id']),
            from_city=event_data.get('fromCity', ''),
            from_detail=event_data.get('fromDetail', ''),
            to_city=event_data.get('toCity', ''),
            to_detail=event_data.get('toDetail', ''),
            contact_method=event_data['contactMethod']
        )
        session.add(new_event)
        session.commit()
        session.refresh(new_event)
        return new_event
    except Exception as e:
        session.rollback()
        raise e
    except Exception as e:
        session.rollback()
        print("資料庫 rollback,原因如下:")
        import traceback
        traceback.print_exc()  # ❗ 印出完整錯誤堆疊
        raise e

def update_event(event):
    session = get_session()
    session.add(event)
    session.commit()