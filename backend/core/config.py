import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    deribit_url: str = Field(..., env="DERIBIT_URL")
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: str = Field(..., env="REDIS_PORT")
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

    @property
    def redis_url(self) -> str:
        """Генерируем стандартный Redis URL из хоста и порта"""
        return f"redis://{self.redis_host}:{self.redis_port}"

    @property
    def sqlalchemy_url(self) -> str:
        return f"postgresql+psycopg2://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
