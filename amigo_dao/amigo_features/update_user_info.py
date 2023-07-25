from amigo_dao.services.dao_services import DaoServices 
from amigo_dao.dataclasse_models.request import AddUserDataClass, UpdateUserInfoDetails
from amigo_dao.amigo_model_creation.sql_models import user_info
from sqlalchemy import Table, update, and_, or_
from sqlalchemy.dialects.postgresql import insert
from amigo_error_handling.errors import InternalServerError

from flask import session


class UpdateUserInfo(DaoServices):
    def update_user_info_after_signup(self, user_data: AddUserDataClass): 
        try:
            with self.engine().begin() as connection:
                user_info_table = Table(
                    user_info,
                    self.metadata(),
                    autoload=True,
                    autoload_with=connection,
                )
                update_query = update(user_info_table).where(user_info_table.c.uid == session.get('uid')).values(
                    first_name = user_data.first_name,
                    middle_name = user_data.middle_name,
                    last_name = user_data.last_name,
                    country_code = user_data.country_code,
                    phone_number = user_data.phone_number,
                    profile_completion_status = user_data.profile_completion_status,
                    preferred_country = user_data.preferred_country,
                    ts_deactivated = user_data.ts_deactivated,
                    ts_updated = user_data.ts_updated,
                    linkedin_profile = user_data.linkedin_profile
                )
                upsert_query_result = connection.execute(update_query)
                return upsert_query_result
        except InternalServerError as e: 
            print("Database Connectivity failed.")
            raise e
        except Exception as e:
            print("Error: ", e)
            raise e
        
    def update_user_info_detials(self, user_data:UpdateUserInfoDetails):
        try:
            with self.engine().begin() as connection:
                user_info_table = Table(
                    user_info,
                    self.metadata(),
                    autoload=True,
                    autoload_with=connection,
                )
                update_query = update(user_info_table).where(user_info_table.c.uid == session.get('uid')).values(
                    field_experience = user_data.field_experience,
                    highest_education = user_data.highest_education,
                    years_experience = user_data.years_experience,
                )
                upsert_query_result = connection.execute(update_query)
                return upsert_query_result
        except InternalServerError as e: 
            print("Database Connectivity failed.")
            raise e
        except Exception as e:
            print("Error: ", e)
            raise e