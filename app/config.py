from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    database_url_sync: str
    parser_service_url: str = "http://localhost:8001"
    parser_service_timeout_seconds: int = 30
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/1"

    model_config = {"env_file": ".env"}


settings = Settings()
