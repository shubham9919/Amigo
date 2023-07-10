from passlib.hash import bcrypt
from flask_login import UserMixin
from sqlalchemy import exc

from amigo_dao.amigo_features.client_login import SignUpUser
from amigo_dao.dataclasse_models.request import ClientSignUpDataClass
from amigo_dao.amigo_features.get_client_login import GetClientLogin
from amigo_error_handling.errors import ConflictError, UnauthorizedError


class User(UserMixin):
    def __init__(self, id_, name, email, last_name):
        self.id = id_
        self.name = name
        self.email = email
        self.last_name = last_name

    @staticmethod
    def get(email, name=None, last_name=None, password=None):
        try:
            if password is not None:
                is_user_exist = GetClientLogin().get_client_login_by_email(email)
                if is_user_exist is not None:
                    if bcrypt.verify(password, is_user_exist.hashed_password):
                        user = User(is_user_exist.uid,name, is_user_exist.email, last_name)
                        return user
                    else:
                        raise UnauthorizedError("Email Id or password is incorrect.")
                else: 
                    return None
            else:
                is_user_exist = GetClientLogin().get_client_login_by_email(email)
                if is_user_exist is not None:
                    user = User(is_user_exist.uid,name, is_user_exist.email, last_name)
                    print("returning user in get--- ", user)
                    return user
                else: 
                    return None
        except Exception as e:
            print("Error: ", e)
            raise e
    
    @staticmethod
    def get_by_id(user_id):
        is_user_exist = GetClientLogin().get_client_login_by_uid(user_id)
        if is_user_exist is not None:
            user = User(is_user_exist.uid, "NA", is_user_exist.email, "NA")
            return user
        else: 
            return None
        
    @staticmethod
    def create(email, name, last_name, password=None):
        try:
            if password is not None:
                user = ClientSignUpDataClass(email, password)
                user_data = SignUpUser().sign_up_user(user)
                user = User(user_data["uid"],name, user_data["email"], last_name)
                print("returning user with password created --- ", user)
                return user
            else:
                user = ClientSignUpDataClass(email, "NA")
                user_data = SignUpUser().sign_up_user(user)
                user = User(user_data["uid"],name, user_data["email"], last_name)
                print("returning user --- ", user)
                return user
        except exc.IntegrityError as e:
            raise ConflictError("User Already Exist")
        except Exception as e:
            print("Error: ", e)
            raise e
    