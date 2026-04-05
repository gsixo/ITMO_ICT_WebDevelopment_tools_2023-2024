import os

from pydantic import model_validator
from pydantic_settings import BaseSettings

from runtime_env import adjust_database_url, adjust_parser_service_url, adjust_redis_url


class Settings(BaseSettings):
    database_url: str
    database_url_sync: str
    parser_service_url: str = "http://parser:8001"
    parser_service_timeout_seconds: float = 30.0
    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"

    model_config = {"env_file": ".env"}

    @model_validator(mode="after")
    def adjust_for_host_runtime(self) -> "Settings":
        self.database_url = adjust_database_url(self.database_url)
        self.database_url_sync = adjust_database_url(self.database_url_sync)
        self.parser_service_url = adjust_parser_service_url(self.parser_service_url)
        self.celery_broker_url = adjust_redis_url(self.celery_broker_url)
        self.celery_result_backend = adjust_redis_url(self.celery_result_backend)

        # Celery reads broker/backend from os.environ and overrides constructor args.
        os.environ["DATABASE_URL"] = self.database_url
        os.environ["DATABASE_URL_SYNC"] = self.database_url_sync
        os.environ["PARSER_SERVICE_URL"] = self.parser_service_url
        os.environ["CELERY_BROKER_URL"] = self.celery_broker_url
        os.environ["CELERY_RESULT_BACKEND"] = self.celery_result_backend
        return self


settings = Settings()
