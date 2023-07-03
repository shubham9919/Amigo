from sqlalchemy import Table, select
from amigo_model_creation.sql_models import (
    user_scores, UserScores
)
from dataclasse_models.response import GetUserScoreResponseDataClass, FetchUserDetailsByUID
from services.dao_services import DaoServices


class GetUserScoreDetails(DaoServices):
    def get_user_score_details(self, userdata: FetchUserDetailsByUID):
        with self.engine().begin() as connection:
            user_info_table = Table(
                user_scores,
                self.metadata(),
                autoload=True,
                autoload_with=connection,
            )
            select_query = select(user_info_table).where(
                user_info_table.c.uid == userdata.uid)
            res_data = connection.execute(select_query).fetchall()
            res_data = res_data[0]
            res_user = GetUserScoreResponseDataClass(res_data[0], res_data[1],  res_data[2], res_data[3], res_data[4])
            return res_user
