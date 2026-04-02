from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/finance_dashboard"

    # JWT
    SECRET_KEY: str = "change-this-secret-key-in-production-use-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # App
    APP_ENV: str = "development"
    APP_TITLE: str = "Finance Dashboard API"
    APP_VERSION: str = "1.0.0"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
