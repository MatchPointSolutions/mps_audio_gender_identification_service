"""
Logger Setup
"""
import logging
from config import LOG_FILE_PATH
import sys


def setup_logger(logger_name, level=logging.INFO):
    """
    Setup the logger and return the logger object.
    """
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')

    # Use StreamHandler to send log messages to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
