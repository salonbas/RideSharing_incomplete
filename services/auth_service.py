#auth_service.py
from dao.users_dao import find_by_username, insert_user
from models.models import User
from werkzeug.security import generate_password_hash, check_password_hash

def login_user(username, password):
    user = find_by_username(username)
    if user and check_password_hash(user.password, password):  # 雜湊比對
        return user
    return None

def find_user_by_username(username):
    return find_by_username(username)

def create_user(username, password, email):
    hashed_password = generate_password_hash(password)  # 雜湊儲存
    user = User(
        username=username,
        password=hashed_password,
        email=email
    )
    return insert_user(user)
