from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings/configuration class"""

    # Database Settings
    POSTGRES_DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres",
        alias="DATABASE_URL",
        description="Database connection string",
    )
    PG_POOL_SIZE: int = Field(default=5, alias="PG_POOL_SIZE")
    PG_POOL_OVERFLOW: int = Field(default=10, alias="PG_POOL_OVERFLOW")
    POSTGRES_SCHEMA: str = Field(default="game_store", alias="POSTGRES_SCHEMA")

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "RealTime Ingestion"
    DEBUG: bool = False

    VERSION: str = "1.0.0"

    # CORS Settings
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000"],
        alias="CORS_ORIGINS",
    )
    CORS_METHODS: list[str] = Field(default=["*"], alias="CORS_METHODS")
    CORS_HEADERS: list[str] = Field(default=["*"], alias="CORS_HEADERS")

    # Cache Settings
    REDIS_URL: str | None = Field(
        default="redis://localhost:6379/0",
        alias="REDIS_URL",
        description="Redis connection string",
    )

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    """
    Creates and returns a cached instance of the settings.
    Use this function to get settings throughout the application.
    """
    return Settings()


settings = Settings()
