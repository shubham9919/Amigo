from sqlalchemy import Table, select

from amigo_dao.amigo_model_creation.sql_models import UserLogin
from amigo_dao.dataclasse_models.response import GetUserLoginDataClass
from amigo_dao.services.dao_services import DaoServices
from amigo_dao.amigo_model_creation.sql_models import user_login


class GetClientLogin(DaoServices):
    def get_client_login_by_email(self, email):
        try:
            with self.engine().begin() as connection:
                user_login_table = Table(
                        user_login,
                        self.metadata(),
                        autoload=True,
                        autoload_with=connection,
                    )
                is_user_exist_query = select(user_login_table).where(user_login_table.c.email == email)
                res_data = connection.execute(is_user_exist_query).fetchall()
                
            if res_data:
                res_data = res_data[0]
                user = GetUserLoginDataClass(res_data["uid"], res_data["email"],res_data["hashed_password"], res_data["ts_added"])
                return user
            else:
                return None
        except Exception as e: 
            print(" get_client_login_by_email Error: ", e)
            raise e

    def get_client_login_by_uid(self, uid):
        try:
            with self.engine().begin() as connection:
                user_login_table = Table(
                        user_login,
                        self.metadata(),
                        autoload=True,
                        autoload_with=connection,
                    )
                is_user_exist_query = select(user_login_table).where(user_login_table.c.uid == uid)
                res_data = connection.execute(is_user_exist_query).fetchall()
                
            if res_data:
                res_data = res_data[0]
                user = GetUserLoginDataClass(res_data["uid"], res_data["email"],res_data["hashed_password"], res_data["ts_added"])
                return user
            else:
                return None
        except Exception as e: 
            print(" get_client_login_by_email Error: ", e)
            raise e