from dao.users_dao import find_by_username_and_password
from config.db import get_session

def login_user(username, password):
    session = get_session()
    return find_by_username_and_password(username, password)
