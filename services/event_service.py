# services/event_service.py
from dao.events_dao import get_all_events, get_event_by_id, update_event
from dao.users_dao import find_by_id

def fetch_events():
    return get_all_events()

def join_or_cancel(user_id, data):
    event_id = data.get("event_id")
    action = data.get("action")
    event = get_event_by_id(event_id)
    user = find_by_id(user_id)
    if not event or not user:
        return {"error": "找不到活動或用戶"}
    if action == "join":
        if event.joinedSeats >= event.requiredSeats:
            return {"error": "活動人數已滿"}
        event.joinedSeats += 1
    elif action == "cancel":
        if event.joinedSeats <= 0:
            return {"error": "無可取消人數"}
        event.joinedSeats -= 1
    else:
        return {"error": "未知的 action"}
    return {"msg": f"{action} 成功"}

