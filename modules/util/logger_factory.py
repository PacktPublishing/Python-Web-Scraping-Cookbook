import logging

def create_default_console_logger(name=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    print("created logger")
    return logger