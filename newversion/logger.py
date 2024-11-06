"""
Set up logging for CLI usage.
"""

import logging

from newversion.constants import LOGGER_NAME


def setup_logging(level: int) -> logging.Logger:
    """
    Set up logging for CLI usage.
    """
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(level)
    formatter = logging.Formatter(
        "%(asctime)s %(name)s: %(levelname)-7s %(message)s", datefmt="%H:%M:%S"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
