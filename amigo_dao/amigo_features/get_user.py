from sqlalchemy import Table, select
from amigo_model_creation.sql_models import (
    user_info, UserInfo
)
from dataclasse_models.response import GetUserResponseDataClass, FetchUserDetailsByUID
from services.dao_services import DaoServices

class GetUserDetails(DaoServices):
    def get_user_details(self, userdata: FetchUserDetailsByUID):
        try:

            with self.engine().begin() as connection:
                user_info_table = Table(
                    user_info,
                    self.metadata(),
                    autoload=True,
                    autoload_with=connection,
                )
                select_query = select(user_info_table).where(user_info_table.c.uid == userdata.uid)
                res_data = connection.execute(select_query).fetchall()
                res_data = res_data[0]
                res_user = GetUserResponseDataClass(
                        res_data[0], res_data[1], res_data[2], res_data[3],
                        res_data[4], res_data[5], res_data[6], res_data[7],
                        res_data[8], res_data[9], res_data[10], res_data[11],
                        res_data[12],res_data[13],res_data[14],res_data[15],
                        res_data[16],res_data[17]
                        )
                return res_user
        except Exception as e: 
            print("Error: ", e)
            raise e  
        
    def get_user_details_by_email(self, email):
        try: 
            with self.engine().begin() as connection:
                user_info_table = Table(
                    user_info,
                    self.metadata(),
                    autoload=True,
                    autoload_with=connection,
                )
                select_query = select(user_info_table).where(user_info_table.c.email == email)
                res_data = connection.execute(select_query).fetchall()
                if res_data is not None:
                    res_data = res_data[0]
                    res_user = GetUserResponseDataClass(
                        res_data[0], res_data[1], res_data[2], res_data[3],
                        res_data[4], res_data[5], res_data[6], res_data[7],
                        res_data[8], res_data[9], res_data[10], res_data[11],
                        res_data[12],res_data[13],res_data[14],res_data[15],
                        res_data[16],res_data[17]
                        )
                    return res_user
                else:
                    return None
        except Exception as e: 
            print(e)
            raise e 