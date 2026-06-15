import os

from pydantic import model_validator
from pydantic_settings import BaseSettings

from runtime_env import adjust_database_url


class Settings(BaseSettings):
    database_url: str
    database_url_sync: str
    parser_service_url: str = "http://localhost:8001"
    parser_service_timeout_seconds: int = 30
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    model_config = {"env_file": ".env"}

    @model_validator(mode="after")
    def adjust_for_host_runtime(self) -> "Settings":
        self.database_url = adjust_database_url(self.database_url)
        self.database_url_sync = adjust_database_url(self.database_url_sync)
        os.environ["DATABASE_URL"] = self.database_url
        os.environ["DATABASE_URL_SYNC"] = self.database_url_sync
        return self


settings = Settings()
