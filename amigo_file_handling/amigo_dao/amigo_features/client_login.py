from amigo_dao.dataclasse_models.request import ClientSignUpDataClass, AddUserDataClass
from amigo_dao.amigo_features.add_user import AddUserDetails
from sqlalchemy import Table, select, and_, insert
from amigo_dao.amigo_model_creation.sql_models import user_login, user_info
from amigo_dao.services.dao_services import DaoServices
from passlib.hash import bcrypt
from datetime import datetime

class SignUpUser(DaoServices):
    def sign_up_user(self, SignUpData:ClientSignUpDataClass):
        # check if the mail id is present in the database already in the userInfo table
        email = SignUpData.email
        with self.engine().begin() as connection:
            user_info_table = Table(
                user_info,
                self.metadata(),
                autoload=True,
                autoload_with=connection,
            )
            user_login_table = Table(
                user_login,
                self.metadata(),
                autoload=True,
                autoload_with=connection,
            )
            is_mailid_exist_query = select(user_info_table).where(user_info_table.c.email == email)
            is_mailid_exist_query_result = connection.execute(is_mailid_exist_query).fetchall()
            if len(is_mailid_exist_query_result) > 0: 
                print(is_mailid_exist_query_result)
                print('user already exist.')
                # Throw error 
            else: 
                # hashing the passowrd 
                if SignUpData.plaintext_password is not None:
                    hashed_password = self.hash_password(SignUpData.plaintext_password)
                    print(hashed_password)
                else:
                    hashed_password = "NA"
                #store the mailId and basic_stage_1 in the user_info table and get the UID
                user = AddUserDataClass(email, None, None, None, None, None, None, 'BASIC_STAGE_1', datetime.now(), None, None, True, None, None, None, None)
                create_user_result = AddUserDetails().add_user_details(user)
                print(create_user_result)
                uid = create_user_result['uid']
                #store the hashed pwd and user email in db along with created uid 
                insert_user_login_query = insert(user_login_table).values(
                    uid = uid,
                    email = email, 
                    hashed_password = hashed_password, 
                    ts_added = datetime.now()
                )
                insert_user_login_query_result = connection.execute(insert_user_login_query)
                return {'uid': uid, 'email': email}



    def hash_password(self, plaintext_password):
        return bcrypt.hash(plaintext_password)