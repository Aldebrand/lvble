import logging
from logging.handlers import RotatingFileHandler
import sys

from config import BASE_LOGGER_CONFIG


def get_logger(logger_name, logger_config=BASE_LOGGER_CONFIG):
    """
    Returns a logger object with the specified name and configuration.

    Args:
        logger_name (str): The name of the logger.
        logger_config (dict): The configuration for the logger. Defaults to BASE_LOGGER_CONFIG.
            The logger_config dictionary should have the following keys:
                - format: The format string for the logger.
                - level: The logging level for the logger.
                - rotating_file_handler: The configuration for the rotating file handler.
                    The rotating_file_handler dictionary should have the following keys:
                        - file_name: The name of the log file.
                        - max_bytes: The maximum size of the log file in bytes.
                        - backup_count: The number of backup log files to keep.

    Returns:
        logging.Logger: The logger object.
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_config['level'])

    formatter = logging.Formatter(logger_config['format'])

    # Create a rotating file handler
    file_handler = RotatingFileHandler(
        logger_config['rotating_file_handler']['file_name'],
        maxBytes=logger_config['rotating_file_handler']['max_bytes'],
        backupCount=logger_config['rotating_file_handler']['backup_count']
    )
    file_handler.setLevel(logger_config['level'])
    file_handler.setFormatter(formatter)

    # Create a stream handler
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
