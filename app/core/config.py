import logging
import sys
from functools import lru_cache
from typing import Optional

from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings

from app.core.logging import logging as logging_config


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


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        """
        Emits a logging record to Loguru.

        Translates the log level, finds the original caller, and logs the message using Loguru.
        """
        try:
            level: str = logger.level(record.levelname).name
        except ValueError:
            level: int = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class LoggingConfig:
    """Logging configuration to be set for the server"""

    # Intercept handler to redirect standard logging to Loguru
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    def set_config_logger(self):
        logger.remove()
        logger.add(
            sys.stdout,
            colorize=True,
            level=logging_config.LOGGER_LEVEL,
            format=logging_config.LOGGER_FORMAT,
        )
