from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.models import User
from config.config import DATABASE_URL

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# 更新前 10 筆使用者的 avatarUrl
for i in range(1, 11):
    user = session.query(User).filter_by(id=i).first()
    if user:
        user.avatarUrl = f"/public/avatars/{i}.png"
        print(f"Updated user {user.username} avatar to {user.avatarUrl}")

session.commit()
session.close()
