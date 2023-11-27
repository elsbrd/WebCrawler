import logging
import os
from logging.handlers import TimedRotatingFileHandler

from core import settings

LOGS_DIR = os.path.join(settings.PROJECT_ROOT, "core/logs")


def setup_logger(name: str) -> logging.Logger:
    """
    Set up a logger with both console and file handlers.

    This function creates a logger with a specific name, sets its level to DEBUG, and adds
    both console and file handlers to it. The console handler logs at INFO level, while
    the file handler logs at DEBUG level and rotates at midnight every day.

    Args:
        name (str): The name of the logger.

    Returns:
        logging.Logger: The configured logger.
    """

    _create_logs_directory()

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)
    c_handler.setFormatter(formatter)

    f_handler = TimedRotatingFileHandler(
        os.path.join(LOGS_DIR, "daily_logs.log"), when="midnight", interval=1
    )
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(formatter)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


def _create_logs_directory():
    """
    Create a directory for log files if it doesn't exist.
    """

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
