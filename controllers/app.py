"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    create_access_token, jwt_required,
    JWTManager, get_jwt_identity
)
import json
import traceback

# === Flask App 基本設定 ===
app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = 'my-super-secret'
jwt = JWTManager(app)

# === 模擬資料庫讀取 ===
with open("db.json", encoding="utf-8") as f:
    data = json.load(f)

users = data['users']
events = data['events']

# === 登入 ===
@app.post("/login")
def login():
    print("✅ 收到 login POST 請求")
    req = request.get_json()
    username = req.get("username")
    password = req.get("password")

    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if not user:
        return jsonify({"msg": "登入失敗"}), 401

    # ✅ identity 用 user['id']，其他資料放進 claims
    access_token = create_access_token(
        identity=str(user['id']),  # ✅ 確保是字串
        additional_claims={
            "username": user['username'],
            "nickname": user.get('nickname', '')
        }
    )

    return jsonify({
        "token": access_token,
        "user": {
            "id": user['id'],
            "username": user['username'],
            "nickname": user.get('nickname', ''),
            "email": user.get('email', ''),
            "avatarUrl": user.get('avatarUrl', ''),
            "instagram": user.get('instagram', ''),
            "phone": user.get('phone', ''),
        }
    })

# === 取得個人檔案 ===
@app.get("/profile")
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({"msg": "使用者不存在"}), 404
    return jsonify(user)

# === 修改個人資料 ===
@app.post("/profile/update")
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        req_data = request.get_json()

        print(f"📝 使用者 {user_id} 嘗試更新個人資料：{req_data}")

        user = next((u for u in users if str(u['id']) == str(user_id)), None)
        if not user:
            return jsonify({"error": "找不到使用者"}), 404

        # ✅ 允許更新的欄位
        updatable_fields = ["nickname", "avatarUrl", "instagram", "email", "phone", "bio"]

        for field in updatable_fields:
            if field in req_data:
                user[field] = req_data[field]

        return jsonify({"msg": "個人資料更新成功", "user": user})

    except Exception as e:
        print(f"❌ 更新個人資料錯誤: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "伺服器錯誤"}), 500

# === 查詢所有活動 ===
@app.get("/events")
def get_events():
    print("📦 傳送活動資料")
    return jsonify(events)

# === 加入或取消活動 ===
@app.post("/events/join")
@jwt_required()
def join_or_cancel_event():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "缺少 JSON 資料"}), 400

        event_id = str(data.get('event_id'))
        action = data.get('action')

        print(f"📩 收到活動請求: event_id={event_id}, action={action}")

        if not event_id or not action:
            return jsonify({"error": "缺少必要欄位"}), 400

        # 取得目前登入者資訊
        user_id = get_jwt_identity()
        user = next((u for u in users if str(u['id']) == str(user_id)), None)
        if not user:
            return jsonify({"error": "用戶未授權"}), 401

        # 查找對應活動
        event = next((e for e in events if str(e['id']) == event_id), None)
        if not event:
            return jsonify({"error": "找不到該活動"}), 404

        print(f"👤 {user['username']} 嘗試 {action} 活動《{event['title']}》")

        if action == 'join':
            if event.get('joinedSeats', 0) >= event.get('requiredSeats', 0):
                return jsonify({"error": "活動人數已滿"}), 400

            event['joinedSeats'] += 1
            print(f"✅ {user['username']} 成功加入活動")
            return jsonify({"msg": f"成功加入活動 {event_id}"}), 200

        elif action == 'cancel':
            if event.get('joinedSeats', 0) > 0:
                event['joinedSeats'] -= 1
                print(f"✅ {user['username']} 成功取消活動")
                return jsonify({"msg": f"成功取消活動 {event_id}"}), 200
            else:
                return jsonify({"error": "無可取消人數"}), 400

        else:
            return jsonify({"error": f"未知的 action: {action}"}), 400

    except Exception as e:
        print(f"❌ 加入活動錯誤: {str(e)}")
        traceback.print_exc()
        return jsonify({"error": f"伺服器錯誤: {str(e)}"}), 500

# === 啟動伺服器 ===
if __name__ == '__main__':
    print("Flask server running at http://localhost:5000")
    app.run(debug=True)
"""
# === controllers/app.py ===
# 三層式架構下的 Controller：負責接收 HTTP 請求，呼叫對應的 service 層邏輯
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from services import auth_service, profile_service, event_service
from config.config import JWT_SECRET_KEY

import services.event_service
print("✅ 目前載入的 event_service 是：", services.event_service.__file__)


app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
jwt = JWTManager(app)

# === 登入 ===
@app.post("/login")
def login():
    req = request.get_json()
    username = req.get("username")
    password = req.get("password")
    user = auth_service.login_user(username, password)

    if not user:
        return jsonify({"msg": "登入失敗"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({
        "token": token,
        "user": user.to_dict()
    })

# === 取得個人檔案 ===
@app.get("/profile")
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = profile_service.get_user_profile(user_id)
    if not user:
        return jsonify({"msg": "使用者不存在"}), 404
    return jsonify(user.to_dict())

# === 修改個人資料 ===
@app.post("/profile/update")
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    updated_user = profile_service.update_user_profile(user_id, data)
    if not updated_user:
        return jsonify({"msg": "找不到使用者"}), 404
    return jsonify({"msg": "更新成功", "user": updated_user.to_dict()})

# === 查詢所有活動 ===
@app.get("/events")
def get_events():
    events = event_service.fetch_events()
    return jsonify([e.to_dict() for e in events])

# === 加入或取消活動 ===
@app.post("/events/join")
@jwt_required()
def join_or_cancel_event():
    user_id = get_jwt_identity()
    data = request.get_json()
    result = event_service.join_or_cancel(user_id, data)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

# === 啟動伺服器 ===
if __name__ == '__main__':
    app.run(debug=True)