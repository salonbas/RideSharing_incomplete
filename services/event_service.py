# services/event_service.py 
from dao.events_dao import get_all_events, get_event_by_id, update_event, create_event
from dao.users_dao import find_by_id
from config.db import get_session

def fetch_events():
    return get_all_events()

def create_new_event(user_id, event_data):  # 新增這個方法
    print("DEBUG: create_new_event called")
    print("DATA: user_id =", user_id)
    print("DATA: event_data =", event_data)
    try:
        event_data['organizer_id'] = user_id
        new_event = create_event(event_data)
        return {"msg": "活動創建成功", "event": new_event.to_dict()}
    except Exception as e:
        return {"error": f"創建活動失敗: {str(e)}"}

def join_or_cancel(user_id, data):
    event_id = data.get("event_id")
    action = data.get("action")
    event = get_event_by_id(event_id)
    session = get_session()
    user = find_by_id(session, user_id)
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
    update_event(event)
    return {"msg": f"{action} 成功"}