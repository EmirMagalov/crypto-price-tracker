import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

sqlalchemy_url = settings.sqlalchemy_url

engine = create_engine(sqlalchemy_url, pool_pre_ping=True)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
