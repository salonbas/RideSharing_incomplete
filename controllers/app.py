# === controllers/app.py ===
# 三層式架構下的 Controller：負責接收 HTTP 請求，呼叫對應的 service 層邏輯
import os
import sys
import re
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from services import auth_service, profile_service, event_service
from config.config import JWT_SECRET_KEY

import services.event_service
print("目前載入的 event_service 是：", services.event_service.__file__)


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
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

# === 取得其他使用者的公開資料 ===
@app.get("/users/<int:user_id>")
def get_public_user(user_id):
    user = profile_service.get_public_user_profile(user_id)
    if not user:
        return jsonify({"msg": "使用者不存在"}), 404
    return jsonify(user)

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
    return jsonify({"msg": "更新成功", "user": updated_user})

@app.post("/profile/avatar")
@jwt_required()
def update_avatar():
    user_id = get_jwt_identity()

    if "avatar" not in request.files:
        return jsonify({"msg": "缺少檔案"}), 400

    file = request.files["avatar"]

    if not file.mimetype.startswith("image/"):
        return jsonify({"msg": "請上傳圖片檔案"}), 400

    try:
        avatar_url = profile_service.handle_avatar_upload(user_id, file)
        return jsonify({"msg": "頭像已更新", "avatarUrl": avatar_url})
    except Exception as e:
        print("❌ 頭像更新失敗:", e)
        return jsonify({"msg": "頭像更新失敗"}), 500

# === 查詢所有活動 ===
@app.get("/events")
def get_events():
    events = event_service.fetch_events()
    return jsonify([e.to_dict() for e in events])

# 在現有的路由中新增這個
@app.post("/events/create")
@jwt_required()
def create_event():
    user_id = get_jwt_identity()
    data = request.get_json()
    result = event_service.create_new_event(user_id, data)
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result), 201

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

@app.post("/register")
def register():
    data = request.get_json()
    username = data.get("username", "")
    password = data.get("password", "")
    email = data.get("email", "")

    # 基本檢查
    if not username or not password or not email:
        return jsonify({"msg": "請填寫所有欄位"}), 400

    # 正規表達式檢查格式
    if not re.fullmatch(r"^[A-Za-z0-9]{1,10}$", username):
        return jsonify({"msg": "帳號格式錯誤:限10字內，僅含英數"}), 400

    if not re.fullmatch(r"^[A-Za-z0-9]{1,8}$", password):
        return jsonify({"msg": "密碼格式錯誤:限8字內，僅含英數"}), 400

    # 檢查帳號是否存在
    if auth_service.find_user_by_username(username):
        return jsonify({"msg": "帳號已被使用"}), 409

    # 創建使用者
    user = auth_service.create_user(username, password, email)

    return jsonify({"msg": "註冊成功", "user": user.to_dict()}), 201

# === 啟動伺服器 ===
if __name__ == '__main__':
    app.run(debug=True)