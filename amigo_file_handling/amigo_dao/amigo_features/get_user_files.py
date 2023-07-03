import json
from sqlalchemy import Table, select, and_
from amigo_model_creation.sql_models import user_files
from dataclasse_models.response import GetUserFilesDataClass, FetchUserFilesByFileType
from services.dao_services import DaoServices

class GetUserFiles(DaoServices): 
    def get_user_files(self, user_data: FetchUserFilesByFileType):
        with self.engine().begin() as connection:
            user_files_table = Table(
                user_files,
                self.metadata(),
                autoload=True,
                autoload_with=connection,
            )
            get_user_files_query =  select(user_files_table).where(and_(
                 user_files_table.c.uid == user_data.uid, user_files_table.c.file_type == user_data.file_type))
            get_user_files_query_result = connection.execute(get_user_files_query).fetchall()
            user_files_data = get_user_files_query_result[0]
            user_files_data = GetUserFilesDataClass(user_files_data[0], user_files_data[1], user_files_data[2])
            s3_endpoints = json.loads(user_files_data.s3_urls)
            return s3_endpoints