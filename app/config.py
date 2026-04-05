from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    database_url_sync: str

    model_config = {"env_file": ".env"}


settings = Settings()
