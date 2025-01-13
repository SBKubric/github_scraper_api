import logging
import logging.config as lconfig
import os
from typing import Any

LOG_FORMAT = "%(asctime)s:%(name)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "error.log")
LOG_DEFAULT_HANDLERS = ["console", "file"]


def get_logging_config(
    log_level: str = LOG_LEVEL,
    log_format: str = LOG_FORMAT,
    handlers: list[str] = LOG_DEFAULT_HANDLERS,
) -> dict[str, Any]:
    """
    Get logging config in dict format.
    """
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": log_format},
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": ("%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s"),
            },
            "json": {
                "format": '{"time": "%(asctime)s", "level": "%(levelname)s", "name": "%(name)s", '
                '"message": "%(message)s", "module": "%(module)s", "funcName": "%(funcName)s"}',
            },
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "file": {
                "level": "INFO",
                "formatter": "verbose",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": LOG_FILE,
                "mode": "a",
                "maxBytes": 10 * 1024 * 1024,  # 10 MB
                "backupCount": 5,
            },
        },
        "loggers": {
            "": {"handlers": handlers, "level": log_level},
            "uvicorn.error": {"level": log_level},
            "uvicorn.access": {
                "handlers": ["console", "file"],
                "level": log_level,
                "propagate": False,
            },
        },
        "root": {"level": log_level, "handlers": handlers},
    }


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Get or initialize a logger.
    """
    if not logging.getLogger().hasHandlers():
        lconfig.dictConfig(get_logging_config())
    return logging.getLogger(name)
