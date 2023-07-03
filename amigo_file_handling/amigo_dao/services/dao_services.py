from amigo_dao.common.utils import read_config_file
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, Session

class DaoServices:
    def __init__(self):
        # will read these props using aws ddb mappings
        self._config = read_config_file()
        self._uri = self._config['RDS_CONNECTION_PROPS']["uri"]
        self._port = self._config['RDS_CONNECTION_PROPS']["port"]
        self._database_type = self._config["RDS_CONNECTION_PROPS"]["database_type"]
        self._database_name = self._config["RDS_CONNECTION_PROPS"]["database_name"]
        self._schema = self._config["RDS_CONNECTION_PROPS"]["schema_name"]
        self._username = self._config["RDS_CONNECTION_PROPS"]["username"]
        self._password = self._config["RDS_CONNECTION_PROPS"]["password"]
        self._engine = create_engine(f'{self._database_type}://{self._username}:'
                                     f'{self._password}@{self._uri}:{self._port}/{self._database_name}', echo=False)

        self._metadata = MetaData(self._engine, schema=self._schema)
    
    def engine(self):
        return self._engine
    
    def metadata(self):
        return self._metadata

    def session(self):
        return sessionmaker(bind=self.engine())
    
    def db_session(self):
        return Session(self.engine())


