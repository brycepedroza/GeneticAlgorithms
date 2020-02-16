import logging
import time
from logging.handlers import RotatingFileHandler

logger = None


# ----------------------------------------------------------------------
def create_rotating_log(path):
    """
    Creates a rotating log
    """
    global logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # add a rotating handler
    handler = RotatingFileHandler(path, backupCount=5, maxBytes=1024*1024)
    logger.addHandler(handler)

