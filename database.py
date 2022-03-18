from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import config

SQLALCHEMY_DATABASE_URL = config.DATABASE_URL


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# mysql - if you want to use it, you should install pymysql
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://username:password@127.0.0.1:3306/db_name"
