這是你剛剛告訴我需要改進的的 🔧 主要改進點
1. 資料庫層面

新增 event_participants 表來記錄用戶參與狀態
使用 UNIQUE(event_id, user_id) 約束確保不重複參加
支援 CASCADE 刪除，活動被刪除時自動清理參與記錄

2. 後端 API 改進

防重複參加：加入前檢查是否已參加
事務處理：確保資料一致性
詳細錯誤處理：提供清楚的錯誤訊息
狀態同步：API 回傳更新後的參與狀態
  請告訴我要分別放到哪個檔案
# === 資料庫模型 - 需要新增一個參與記錄表 ===
"""
CREATE TABLE event_participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE(event_id, user_id)  -- 確保同一個用戶不能重複參加同一個活動
);
"""

# === 後端 API 改進版 ===
from sqlalchemy import text

@app.post("/events/action")
@jwt_required()
def handle_event_action():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    result = event_service.handle_event_action(user_id, data)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

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
    existing_participation = session.execute(
        text("SELECT id FROM event_participants WHERE event_id = :event_id AND user_id = :user_id"),
        {"event_id": event.id, "user_id": user_id}
    ).fetchone()
    
    if existing_participation:
        return {"error": "您已經參加過這個活動了"}
    
    try:
        # 開始事務
        session.begin()
        
        # 新增參與記錄
        session.execute(
            text("INSERT INTO event_participants (event_id, user_id) VALUES (:event_id, :user_id)"),
            {"event_id": event.id, "user_id": user_id}
        )
        
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
    participation = session.execute(
        text("SELECT id FROM event_participants WHERE event_id = :event_id AND user_id = :user_id"),
        {"event_id": event.id, "user_id": user_id}
    ).fetchone()
    
    if not participation:
        return {"error": "您尚未參加這個活動"}
    
    try:
        # 開始事務
        session.begin()
        
        # 刪除參與記錄
        session.execute(
            text("DELETE FROM event_participants WHERE event_id = :event_id AND user_id = :user_id"),
            {"event_id": event.id, "user_id": user_id}
        )
        
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
        # 開始事務
        session.begin()
        
        # 刪除所有參與記錄（CASCADE 會自動處理）
        delete_event_by_id(session, event.id)
        
        # 提交事務
        session.commit()
        
        return {"msg": "活動已成功取消"}
        
    except Exception as e:
        session.rollback()
        print(f"刪除活動失敗: {e}")
        return {"error": "刪除活動失敗，請稍後再試"}

# === 新增：獲取用戶參加的活動列表 ===
@app.get("/events/joined")
@jwt_required()
def get_joined_events():
    user_id = int(get_jwt_identity())
    session = get_session()
    
    try:
        # 獲取用戶參加的所有活動ID
        joined_event_ids = session.execute(
            text("SELECT event_id FROM event_participants WHERE user_id = :user_id"),
            {"user_id": user_id}
        ).fetchall()
        
        event_ids = [row[0] for row in joined_event_ids]
        
        return jsonify({
            "joinedEventIds": event_ids
        })
        
    except Exception as e:
        print(f"獲取參加活動列表失敗: {e}")
        return jsonify({"error": "獲取參加活動列表失敗"}), 500
    finally:
        session.close()

# === 修改活動詳情API，包含參與狀態 ===
@app.get("/events/<int:event_id>")
@jwt_required(optional=True)
def get_event_detail(event_id):
    user_id = get_jwt_identity()
    session = get_session()
    
    try:
        event = get_event_by_id(session, event_id)
        if not event:
            return jsonify({"error": "找不到活動"}), 404
        
        # 檢查當前用戶是否已參加
        has_joined = False
        if user_id:
            participation = session.execute(
                text("SELECT id FROM event_participants WHERE event_id = :event_id AND user_id = :user_id"),
                {"event_id": event_id, "user_id": int(user_id)}
            ).fetchone()
            has_joined = participation is not None
        
        event_data = {
            # ... 其他活動資料
            "hasJoined": has_joined,
            "joinedSeats": event.joinedSeats,
            "spotsRemaining": event.requiredSeats - event.joinedSeats
        }
        
        return jsonify(event_data)
        
    except Exception as e:
        print(f"獲取活動詳情失敗: {e}")
        return jsonify({"error": "獲取活動詳情失敗"}), 500
    finally:
        session.close()