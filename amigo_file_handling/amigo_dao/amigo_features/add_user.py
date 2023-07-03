from sqlalchemy import Table, insert
from amigo_dao.services.dao_services import DaoServices
from amigo_dao.dataclasse_models.request import AddUserDataClass
from amigo_dao.amigo_model_creation.sql_models import UserInfo, user_info

class AddUserDetails(DaoServices):
    def add_user_details(self, user_data: AddUserDataClass):
        with self.engine().begin() as connection:
            user_info_table = Table(
                user_info,
                self.metadata(),
                autoload=True,
                autoload_with=connection,
            )
            add_user_query = insert(UserInfo).values(
                first_name = user_data.first_name,
                middle_name = user_data.middle_name,
                last_name = user_data.last_name,
                email = user_data.email,
                country_code = user_data.country_code,
                phone_number = user_data.phone_number,
                profile_completion_status = user_data.profile_completion_status,
                ts_added = user_data.ts_added,
                preferred_country = user_data.preferred_country,
                ts_deactivated = user_data.ts_deactivated,
                ts_updated = user_data.ts_updated,
                is_active = user_data.is_active
                ).returning(
                    user_info_table.c.uid,
                    user_info_table.c.email,
                    user_info_table.c.profile_completion_status
                )
            result = connection.execute(add_user_query)
            [uid, email, profile_completion_status] = result.fetchone()
            return {
                "uid": uid, 
                "email": email,
                "profile_completion_status": profile_completion_status
            }
