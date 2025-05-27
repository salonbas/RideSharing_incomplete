# === dao/user_dao.py ===
from models.models import User
from config.db import get_session

def find_by_id(user_id):
    session = get_session()
    return session.query(User).filter_by(id=user_id).first()

def find_by_username(username):
    session = get_session()
    return session.query(User).filter_by(username=username).first()

def insert_user(user):
    session = get_session()
    session.add(user)
    session.commit()
    session.refresh(user)  #讓 user 可安全回傳給前端
    return user

def update_user(user):
    session = get_session()
    session.add(user)
    session.commit()
    return user
