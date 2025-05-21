from dao.users_dao import find_by_id, update_user

def get_user_profile(user_id):
    return find_by_id(user_id)

def update_user_profile(user_id, data):
    user = find_by_id(user_id)
    if not user:
        return None
    for field in ["nickname", "avatarUrl", "instagram", "email", "phone", "bio"]:
        if field in data:
            setattr(user, field, data[field])
    return update_user(user)






