from sqlalchemy import Table
from sqlalchemy.dialects.postgresql import insert

from amigo_dao.services.dao_services import DaoServices
from amigo_dao.amigo_model_creation.sql_models import user_scores
from amigo_dao.dataclasse_models.request import AddUserGradesDataClass

class AddUserGrades(DaoServices): 
    def add_user_grades(self, grades: list[AddUserGradesDataClass]):
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