# services/event_service.py 
from dao.events_dao import (
    get_all_events, get_event_by_id, update_event, create_event, 
    delete_event_by_id, check_user_participation, add_participation, 
    remove_participation, get_user_joined_event_ids
)
from dao.users_dao import find_by_id
from config.db import get_session

def fetch_events():
    session = get_session()
    return get_all_events(session)

def create_new_event(user_id, event_data):  
    print("DEBUG: create_new_event called")
    print("DATA: user_id =", user_id)
    print("DATA: event_data =", event_data)
    session = get_session()
    try:
        event_data['organizer_id'] = user_id
        new_event = create_event(session, event_data)
        return {"msg": "活動創建成功", "event": new_event.to_dict()}
    except Exception as e:
        return {"error": f"創建活動失敗: {str(e)}"}

def get_user_events(user_id):
    """獲取用戶的活動（創建的和參加的）"""
    session = get_session()
    try:
        user = find_by_id(session, user_id)
        if not user:
            return {"error": "找不到使用者"}

        # 獲取用戶創建的活動
        organized_events = []
        if hasattr(user, 'events') and user.events:
            organized_events = [event.to_dict() for event in user.events]
        
        # 獲取用戶參加的活動
        joined_events = []
        if hasattr(user, 'joined_events') and user.joined_events:
            joined_events = [participant.event.to_dict() for participant in user.joined_events if participant.event]
        
        print(f" User {user_id} events: organized={len(organized_events)}, joined={len(joined_events)}")
        
        return {
            "organized": organized_events,
            "joined": joined_events
        }
        
    except Exception as e:
        print(f"❌ get_user_events error: {e}")
        return {"error": f"獲取用戶活動失敗: {str(e)}"}
    finally:
        session.close()    

def handle_event_action(user_id, data):
    event_id = data.get("event_id")
    action = data.get("action")
    session = get_session()
    
    try:
        event = get_event_by_id(session, event_id)
        user = find_by_id(session, user_id)
        
        if not event or not user:
            print(f"找不到活動或用戶 event_id: {event_id}, user_id: {user_id}")
            return {"error": "找不到活動或用戶"}
        
        if action == "join":
            return handle_join_event(session, event, user_id)
        elif action == "cancel":
            return handle_leave_event(session, event, user_id)
        elif action == "delete":
            return handle_delete_event(session, event, user_id)
        else:
            return {"error": f"未知的 action: {action}"}
            
    except Exception as e:
        session.rollback()
        print(f"處理活動操作時發生錯誤: {e}")
        return {"error": "操作失敗，請稍後再試"}
    finally:
        session.close()

def handle_join_event(session, event, user_id):
    """處理加入活動"""
    # 檢查活動是否已滿
    if event.joinedSeats >= event.requiredSeats:
        return {"error": "活動人數已滿"}
    
    # 檢查用戶是否已經參加過這個活動
    existing_participation = check_user_participation(session, event.id, user_id)
    if existing_participation:
        return {"error": "您已經參加過這個活動了"}
    
    try:
        # 新增參與記錄
        add_participation(session, event.id, user_id)
        
        # 更新活動參與人數
        event.joinedSeats += 1
        update_event(session, event)
        
        # 提交事務
        session.commit()
        
        return {
            "msg": "加入成功",
            "hasJoined": True,
            "joinedSeats": event.joinedSeats,
            "spotsRemaining": event.requiredSeats - event.joinedSeats
        }
        
    except Exception as e:
        session.rollback()
        print(f"加入活動失敗: {e}")
        return {"error": "加入活動失敗，請稍後再試"}

def handle_leave_event(session, event, user_id):
    """處理退出活動"""
    # 檢查用戶是否已經參加這個活動
    participation = check_user_participation(session, event.id, user_id)
    if not participation:
        return {"error": "您尚未參加這個活動"}
    
    try:
        # 刪除參與記錄
        remove_participation(session, event.id, user_id)
        
        # 更新活動參與人數
        event.joinedSeats = max(0, event.joinedSeats - 1)
        update_event(session, event)
        
        # 提交事務
        session.commit()
        
        return {
            "msg": "退出成功",
            "hasJoined": False,
            "joinedSeats": event.joinedSeats,
            "spotsRemaining": event.requiredSeats - event.joinedSeats
        }
        
    except Exception as e:
        session.rollback()
        print(f"退出活動失敗: {e}")
        return {"error": "退出活動失敗，請稍後再試"}

def handle_delete_event(session, event, user_id):
    """處理刪除活動"""
    if event.organizer_id != user_id:
        print(f"[DEBUG] Current organizer_id: {event.organizer_id}")
        print(f"[DEBUG] Current      user_id: {user_id}")
        return {"error": "只有主辦人可以取消活動"}
    
    try:
        # 刪除活動（CASCADE 會自動處理參與記錄）
        delete_event_by_id(session, event.id)
        
        # 提交事務
        session.commit()
        
        return {"msg": "活動已成功取消"}
        
    except Exception as e:
        session.rollback()
        print(f"刪除活動失敗: {e}")
        return {"error": "刪除活動失敗，請稍後再試"}

# 新增：獲取用戶已參加的活動ID列表
def get_user_joined_events(user_id):
    """獲取用戶參加的活動ID列表"""
    session = get_session()
    try:
        event_ids = get_user_joined_event_ids(session, user_id)
        return {"joinedEventIds": event_ids}
    except Exception as e:
        print(f"獲取參加活動列表失敗: {e}")
        return {"error": "獲取參加活動列表失敗"}
    finally:
        session.close()

# 新增：獲取活動詳情包含參與狀態
def get_event_with_participation(event_id, user_id=None):
    """獲取活動詳情，包含用戶參與狀態"""
    session = get_session()
    try:
        event = get_event_by_id(session, event_id)
        if not event:
            return {"error": "找不到活動"}
        
        # 檢查當前用戶是否已參加
        has_joined = False
        if user_id:
            participation = check_user_participation(session, event_id, int(user_id))
            has_joined = participation is not None
        
        event_data = event.to_dict()
        event_data.update({
            "hasJoined": has_joined,
            "joinedSeats": event.joinedSeats,
            "spotsRemaining": event.requiredSeats - event.joinedSeats
        })
        
        return event_data
        
    except Exception as e:
        print(f"獲取活動詳情失敗: {e}")
        return {"error": "獲取活動詳情失敗"}
    finally:
        session.close()