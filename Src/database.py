import pymysql
from Src.models.databases import *
from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from Src import config

pymysql.install_as_MySQLdb()
engine = create_engine(
    config.MYSQL_URL,
    pool_size=config.MYSQL_POOL_SIZE,
    max_overflow=config.MYSQL_MAX_OVERFLOW,
    pool_recycle=config.MYSQL_POOL_RECYCLE
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]