import json
from sqlalchemy import Table, update, select, and_
from services.dao_services import DaoServices
from amigo_model_creation.sql_models import user_files
from dataclasse_models.request import UpdateUserFilesDataClass


class UpdateUserFiles(DaoServices):
    def update_user_files(self, user_data: UpdateUserFilesDataClass):
        try:
            with self.engine().begin() as connection:
                user_files_table = Table(
                    user_files,
                    self.metadata(),
                    autoload=True,
                    autoload_with=connection,
                )
                # fetch details
                get_user_files_query = select(user_files_table).where(and_(
                    user_files_table.c.uid == user_data.uid, user_files_table.c.file_type == user_data.file_type))

                user_files_data = connection.execute(
                    get_user_files_query).fetchall()
                user_files_data = user_files_data[0]
                user_files_data = UpdateUserFilesDataClass(
                    user_files_data[0], user_files_data[1], user_files_data[2], None)
                # append the s3 url
                s3_urls = json.loads(user_files_data.s3_urls)
                s3_urls[user_data.file_name] = user_data.s3_urls
                updated_s3_urls = json.dumps(s3_urls)
                # update detail
                update_user_files_query = update(user_files_table).where(
                    and_(user_files_table.c.uid == user_data.uid, user_files_table.c.file_type == user_data.file_type)).values(
                        s3_urls=updated_s3_urls
                )
                update_user_files_result = connection.execute(
                    update_user_files_query)
                return update_user_files_result
        except Exception as e: 
            print("Error: ", e)
            raise e 

