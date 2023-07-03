from typing import TypedDict, Optional
from dataclasses import dataclass, astuple
from datetime import datetime
from flask_login import UserMixin

from amigo_dao.amigo_features.client_login import SignUpUser


@dataclass
class LoginUser(UserMixin):
    uid: int
    name: str
    last_name: str
    email: str

@staticmethod
def get(self, user_id):
    # db = get_db()
    # user = db.execute(
    #     "SELECT * FROM user WHERE id = ?", (user_id,)
    # ).fetchone()
    # if not user:
    #     return None
    
    user = LoginUser(
        uid=5, name="Deepak", email="mine@gmail.com", last_name="chavan"
    )
    return user

@staticmethod
def create(self, user):
    user_data = SignUpUser().sign_up_user(user)

@staticmethod
def get_id(self):
        return LoginUser.uid
    