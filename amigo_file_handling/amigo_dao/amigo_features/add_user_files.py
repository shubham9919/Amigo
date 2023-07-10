import json
from sqlalchemy import Table, exc
from sqlalchemy.dialects.postgresql import insert

from amigo_dao.services.dao_services import DaoServices
from amigo_dao.amigo_model_creation.sql_models import user_files
from amigo_dao.dataclasse_models.request import AddUserFilesDataClass
from amigo_error_handling.errors import InternalServerError, ConflictError


class AddUserFiles(DaoServices): 

    def add_user_files(self, user_data: list[AddUserFilesDataClass]): 
        try:
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
        except InternalServerError as e: 
            print("Database Connectivity failed.")
            raise e
        except exc.IntegrityError as e:
            raise ConflictError("Record already exist for the user")
        except Exception as e:
            print("Error: ", e)
            raise e