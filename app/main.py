# fastapi add router
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.api.exceptions import validation_exception_handler
from app.api.main import api_router
from app.core.config import get_settings
from app.core.events import shutdown_db_clients, startup_db_clients
from app.core.logging import set_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application")
    await startup_db_clients(app)
    yield
    logger.info("Stopping application")
    await shutdown_db_clients(app)


def get_application() -> FastAPI:
    """Returns a FastAPI application instance."""
    settings = get_settings()
    set_logger()
    app = FastAPI(
        description=settings.PROJECT_NAME,
        version=settings.VERSION,
        lifespan=lifespan,
        debug=settings.DEBUG,
        docs_url="/docs",
    )

    app.include_router(api_router)

    if settings.CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_methods=settings.CORS_METHODS,
            allow_headers=settings.CORS_HEADERS,
            allow_credentials=True,
        )

    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    return app


app = get_application()
