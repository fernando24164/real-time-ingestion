from functools import lru_cache
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings/configuration class"""

    POSTGRES_AUTH: dict = {"user": "postgres", "password": "mysecretpassword"}
    POSTGRES_DATABASE_URL: str = f"postgresql+asyncpg://{POSTGRES_AUTH.get('user')}:{POSTGRES_AUTH.get('password')}@localhost:5432"
    PG_POOL_SIZE: int = 5
    PG_POOL_OVERFLOW: int = 10

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "RealTime Ingestion"
    DEBUG: bool = False

    VERSION: str = "1.0.0"

    # CORS Settings
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]
    CORS_METHODS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]

    # Cache Settings
    REDIS_URL: Optional[str] = Field(
        default="redis://localhost:6379", description="Redis connection string"
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Creates and returns a cached instance of the settings.
    Use this function to get settings throughout the application.
    """
    return Settings()
