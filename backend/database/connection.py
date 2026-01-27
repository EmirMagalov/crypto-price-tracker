import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

DB_USER = settings.db_user
DB_NAME = settings.db_name
DB_PASSWORD = settings.db_password
DB_PORT = settings.db_port
DB_HOST = settings.db_host
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
