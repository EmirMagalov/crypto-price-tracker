import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    deribit_url: str = Field(..., env="DERIBIT_URL")
    base_redis: str = Field(..., env="BASE_REDIS")
    redis_celery_0: str = Field(..., env="REDIS_CELERY_0")
    redis_celery_1: str = Field(..., env="REDIS_CELERY_1")
    db_user: str = Field(..., env="DB_USER")
    db_name: str = Field(..., env="DB_NAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_port: int = Field(..., env="DB_PORT")
    db_host: str = Field(..., env="DB_HOST")
    frontend_origins: str = Field(..., env="FRONTEND_ORIGINS")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), "../../.env"),
        env_file_encoding="utf-8",
        extra="allow",  # теперь лишние поля из .env не вызывают ошибку
    )


settings = Settings()
