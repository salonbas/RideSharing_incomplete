# === dao/user_dao.py ===
from models.models import User
from sqlalchemy.orm import Session
from config.db import get_session

def find_by_username_and_password(username, password):
    session = get_session()
    return session.query(User).filter_by(username=username, password=password).first()

def find_by_id(user_id):
    session = get_session()
    return session.query(User).filter_by(id=user_id).first()

def update_user(user):
    session = get_session()
    session.add(user)
    session.commit()
    return user
