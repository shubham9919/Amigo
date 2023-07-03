from flask_login import UserMixin

from amigo_dao.amigo_features.client_login import SignUpUser
from amigo_dao.dataclasse_models.request import ClientSignUpDataClass
from amigo_dao.amigo_features.get_client_login import GetClientLogin


class User(UserMixin):
    def __init__(self, id_, name, email, last_name):
        self.id = id_
        self.name = name
        self.email = email
        self.last_name = last_name

    @staticmethod
    def get(email, name, last_name):
        is_user_exist = GetClientLogin().get_client_login_by_email(email)
        if is_user_exist is not None:
            user = User(is_user_exist["uid"],name, is_user_exist["email"], last_name)
            return user
        else: 
            return None

    @staticmethod
    def create(email, name, last_name):
        user = ClientSignUpDataClass(email, "NA")
        user_data = SignUpUser().sign_up_user(user)
        user = User(user_data["uid"],name, user_data["email"], last_name)
        return user