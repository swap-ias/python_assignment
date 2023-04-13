import logging


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logging.basicConfig(format="%(levelname)s | %(asctime)s | %(message)s")
    return logger
