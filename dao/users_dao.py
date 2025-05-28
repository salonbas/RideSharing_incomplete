# dao/users_dao.py
from models.models import User

def find_by_id(session, user_id):
    return session.query(User).filter_by(id=user_id).first()

def find_by_username(session, username):
    return session.query(User).filter_by(username=username).first()

def insert_user(session, user):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def update_user(session, user):
    session.add(user)
    session.commit()
    return user
