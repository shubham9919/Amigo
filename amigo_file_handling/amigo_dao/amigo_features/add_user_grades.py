from sqlalchemy import Table, exc
from sqlalchemy.dialects.postgresql import insert

from amigo_dao.services.dao_services import DaoServices
from amigo_dao.amigo_model_creation.sql_models import user_scores
from amigo_dao.dataclasse_models.request import AddUserGradesDataClass
from amigo_error_handling.errors import InternalServerError, ConflictError

class AddUserGrades(DaoServices): 
    def add_user_grades(self, grades: list[AddUserGradesDataClass]):
        try:
            with self.engine().begin() as connection:
                user_scores_table = Table(
                    user_scores,
                    self.metadata(),
                    autoload=True,
                    autoload_with=connection,
                )
                add_score_query = insert(user_scores_table, grades)
                response = connection.execute(add_score_query)
                return response
        except InternalServerError as e: 
            print("Database Connectivity failed.")
            raise e
        except exc.IntegrityError as e:
            raise ConflictError("Record already exist for the user")
        except Exception as e:
            print("Error: ", e)
            raise e