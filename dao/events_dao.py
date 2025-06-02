# === dao/event_dao.py ===
from models.models import Event, EventParticipant
from config.db import get_session
from datetime import datetime
from sqlalchemy import text

def get_all_events(session):
    return session.query(Event).all()

def get_event_by_id(session, event_id):
    return session.query(Event).filter_by(id=event_id).first()

def create_event(session, event_data): 
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
        print("資料庫 rollback,原因如下:")
        import traceback
        traceback.print_exc()
        raise e

def update_event(session, event):
    session.add(event)
    session.commit()

def delete_event_by_id(session, event_id):
    print(f"DEBUG: 進入 delete_event_by_id，準備刪除活動 ID = {event_id}")
    try:
        event = session.query(Event).filter_by(id=event_id).first()
        if not event:
            print(f"WARNING: 找不到活動 ID = {event_id}，無法刪除")
            return False
        session.delete(event)
        session.commit()
        print(f" 活動 ID = {event_id} 刪除成功")
        return True
    except Exception as e:
        session.rollback()
        print(" 刪除活動時發生錯誤，資料庫已 rollback")
        import traceback
        traceback.print_exc()
        return False

# 新增：檢查用戶是否已參加活動
def check_user_participation(session, event_id, user_id):
    """檢查用戶是否已參加指定活動"""
    return session.query(EventParticipant).filter_by(
        event_id=event_id, 
        user_id=user_id
    ).first()

# 新增：新增參與記錄
def add_participation(session, event_id, user_id):
    """新增用戶參與記錄"""
    participation = EventParticipant(event_id=event_id, user_id=user_id)
    session.add(participation)
    return participation

# 新增：移除參與記錄
def remove_participation(session, event_id, user_id):
    """移除用戶參與記錄"""
    participation = session.query(EventParticipant).filter_by(
        event_id=event_id, 
        user_id=user_id
    ).first()
    if participation:
        session.delete(participation)
        return True
    return False

# 新增：取得用戶參加的活動ID列表
def get_user_joined_event_ids(session, user_id):
    """取得用戶參加的所有活動ID"""
    participations = session.query(EventParticipant.event_id).filter_by(user_id=user_id).all()
    return [p.event_id for p in participations]