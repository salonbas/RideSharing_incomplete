# === 專案初始化：三層式分層架構啟動 ===
# 此檔案為 init_db.py，用於初次從 db.json 初始化 app.db

import json
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, User, Event
from config.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

with open("db.json", encoding="utf-8") as f:
    data = json.load(f)

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

for e in data["events"]:
    event = Event(
        id=e["id"],
        title=e["title"],
        description=e.get("description", ""),
        type=e.get("type", ""),
        date=datetime.fromisoformat(e["date"]),
        requiredSeats=e.get("requiredSeats", 0),
        joinedSeats=e.get("joinedSeats", 0),
        organizer=user_dict[e["userId"]]
    )
    session.add(event)

session.commit()
print("✅ 資料庫初始化完成")