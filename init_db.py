# === 專案初始化：三層式分層架構啟動 ===
# 此檔案為 init_db.py，用於初次從 db.json 初始化 app.db

import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, Event
from config.config import DATABASE_URL

# 建立資料庫連線
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# 重建所有資料表
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# 讀取 JSON 檔案
with open("db.json", encoding="utf-8") as f:
    data = json.load(f)

# 儲存 user 實體以供後續 event 使用
user_dict = {}
for u in data["users"]:
    user = User(
        id=u["id"],
        username=u["username"],
        password=u["password"],
        nickname=u.get("nickname", ""),
        avatarUrl=u.get("avatarUrl", ""),
        instagram=u.get("instagram", ""),
        email=u.get("email", ""),
        phone=u.get("phone", ""),
        bio=u.get("bio", "")
    )
    user_dict[u["id"]] = user
    session.add(user)

# 新增活動資料，包含地點資訊
for e in data["events"]:
    event = Event(
        id=e["id"],
        title=e["title"],
        description=e.get("description", ""),
        type=e.get("type", ""),
        date=datetime.fromisoformat(e["date"]),
        requiredSeats=e.get("requiredSeats", 0),
        joinedSeats=e.get("joinedSeats", 0),
        organizer=user_dict[e["userId"]],
        from_city=e.get("location", {}).get("from", {}).get("city", ""),
        from_detail=e.get("location", {}).get("from", {}).get("detail", ""),
        to_city=e.get("location", {}).get("destination", {}).get("city", ""),
        to_detail=e.get("location", {}).get("destination", {}).get("detail", "")
    )
    session.add(event)

# 提交變更
session.commit()
print("✅ 資料庫初始化完成")