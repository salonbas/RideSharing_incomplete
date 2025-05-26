#services/profile_service.py
from dao.users_dao import find_by_id, update_user
from config.db import get_session
import os, uuid
from werkzeug.utils import secure_filename

def get_user_profile(user_id):
    session = get_session()
    return find_by_id(session, user_id)

def get_public_user_profile(user_id):
    session = get_session()
    user = find_by_id(session, user_id)
    return user.to_public_dict() if user else None

def update_user_profile(user_id, data):
    with get_session() as session:
        user = find_by_id(session, user_id)
        if not user:
            return None

        for field in ["nickname", "avatarUrl", "instagram", "email", "phone", "bio"]:
            if field in data:
                setattr(user, field, data[field])

        update_user(session, user)
        return user.to_dict()

def handle_avatar_upload(user_id, file):
    with get_session() as session:
        user = find_by_id(session, user_id)
        if not user:
            raise Exception("找不到使用者")

        # 儲存新頭像
        ext = os.path.splitext(secure_filename(file.filename))[1] or ".png"
        filename = f"{uuid.uuid4().hex}{ext}"
        upload_dir = os.path.join(os.getcwd(), "public", "avatars")
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, filename)
        file.save(save_path)

        # 刪除舊檔
        old_avatar = user.avatarUrl
        if old_avatar and "/avatars/" in old_avatar:
            old_path = os.path.join(os.getcwd(), "public", old_avatar.lstrip("/"))
            if os.path.exists(old_path):
                try:
                    os.remove(old_path)
                except Exception as e:
                    print(f"⚠️ 刪除舊頭像失敗: {e}")

        # 更新欄位 → 呼叫 DAO 寫入
        user.avatarUrl = f"/avatars/{filename}"
        update_user(session, user)

        return user.avatarUrl

