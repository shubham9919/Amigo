import json
from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import insert

from amigo_dao.services.dao_services import DaoServices
from amigo_dao.amigo_model_creation.sql_models import user_files
from amigo_dao.dataclasse_models.request import AddUserFilesDataClass

class AddUserFiles(DaoServices): 
    def add_user_files(self, user_data: list[AddUserFilesDataClass]): 
        with self.engine().begin() as connection:
            user_files_table = Table(
                user_files,
                self.metadata(),
                autoload=True,
                autoload_with=connection,
            )
            insert_user_files_query = insert(user_files_table, user_data)
            insert_user_files_result = connection.execute(insert_user_files_query)
        return insert_user_files_result