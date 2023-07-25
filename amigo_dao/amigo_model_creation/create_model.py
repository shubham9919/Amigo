from sql_models import Base
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy import MetaData

engine = create_engine("postgresql://postgres:admin@localhost:5432/amigo", echo=True)
metadata = MetaData(schema='test22')
session = Session(engine)
session.execute(text('SET search_path TO test22'))
session.commit()
Base.metadata.create_all(engine)
session.close()
