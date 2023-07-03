from sqlalchemy import (
    BigInteger,
    Boolean,
    INT,
    SmallInteger,
    Column,
    DateTime,
    ForeignKeyConstraint,
    MetaData,
    func,
    VARCHAR
)
from amigo_dao.common.constants import (
    user_info,
    user_login,
    user_files,
    user_scores
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(metadata=MetaData(schema='test22'))

class UserInfo(Base):
    __tablename__ = "user_info"
    uid = Column(BigInteger(), autoincrement=True, primary_key=True)
    email = Column(VARCHAR, nullable=False)
    first_name = Column(VARCHAR(255))
    middle_name = Column(VARCHAR(255))
    last_name = Column(VARCHAR(255))
    country_code = Column(VARCHAR(5))
    phone_number = Column(BigInteger())
    preferred_country = Column(VARCHAR(255))
    profile_completion_status = Column(VARCHAR(255), nullable=False)
    ts_added = Column(DateTime, default=func.now())
    ts_updated = Column(DateTime)
    ts_deactivated = Column(DateTime)
    is_active = Column(Boolean, nullable=False)

class UserScores(Base):
    __tablename__ = "user_scores"
    uid = Column(
        BigInteger(),
        primary_key=True)
    exam = Column(VARCHAR(255), primary_key=True)
    appeared_on = Column(DateTime)
    __table_args__ = (
        ForeignKeyConstraint(
            ["uid"],
            ["user_info.uid"],
        ),
    )

class UserLogin(Base):
    __tablename__ = "user_login"
    uid = Column(
        BigInteger(),
        primary_key=True,)
    email = Column(VARCHAR, nullable=False)
    hashed_password = Column(VARCHAR, nullable=False)
    ts_added = Column(DateTime, default=func.now())
    __table_args__ = (
        ForeignKeyConstraint(
            ["uid"],
            ["user_info.uid"],
        ),
    )


class UserFiles(Base):
    __tablename__ = "user_files"
    uid = Column(
        BigInteger(),
        primary_key=True)
    file_type = Column(VARCHAR(20),  primary_key=True, nullable=False)
    s3_urls = Column(VARCHAR, nullable=False)
    __table_args__ = (
        ForeignKeyConstraint(
            ["uid"],
            ["user_info.uid"],
        ),
    )
