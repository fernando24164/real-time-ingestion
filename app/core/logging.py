import logging
import os
import sys

from loguru import logger

logger.remove()
logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")


class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def set_logger():
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(handlers=[InterceptHandler()], level=log_level)

    loggers = [
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "gunicorn",
        "gunicorn.access",
        "gunicorn.error",
    ]

    for logger_name in loggers:
        logging.getLogger(logger_name).handlers = [InterceptHandler()]
