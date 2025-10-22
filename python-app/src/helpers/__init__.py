import logging
import sys
from logging import Logger


def create_logger(provider_name: str, level: int = logging.INFO) -> Logger:
    logger = logging.getLogger(provider_name)
    logger.setLevel(level)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    return logger


logger = create_logger("catch-all-logger")
