# we can import User as the 'user.py' is within the same directory as this None

from models.user import UserModel
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):   # true if they are the same
        return user

def identity(payload):
    print(payload)
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
