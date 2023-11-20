"""
Logger Setup
"""
import logging
from config import LOG_FILE_PATH


def setup_logger(logger_name, log_file=LOG_FILE_PATH, level=logging.INFO):
    """
    Setup the logger and return the logger object.
    """
    formatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger
