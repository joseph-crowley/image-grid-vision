import logging
import os

def setup_logger(filename):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s')
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    handler = logging.FileHandler(filename)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger