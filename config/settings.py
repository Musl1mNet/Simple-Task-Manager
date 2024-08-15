import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from elasticsearch import Elasticsearch
DOTENV = os.path.join(os.path.dirname(__file__), ".env")


class Settings(BaseSettings):
    es_host: str = Field(...)
    secret_key: str = Field(...)
    algorithm: str = Field(..., alias="JWT_ALGORITHM")
    access_token_expire_minutes: int = 30
    user_index: str = Field(..., alias="USER_INDEX_NAME")
    task_index: str = Field(..., alias="TASK_INDEX_NAME")
    model_config = SettingsConfigDict(
        env_file=DOTENV, env_file_encoding="utf-8", extra="allow")


es = Elasticsearch(hosts=[str(Settings().es_host),])
settings = Settings()
