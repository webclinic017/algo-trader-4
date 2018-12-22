import logging
import logging.handlers

from algotrader import logger


FORMAT = "[%(asctime)s] Thread(%(threadName)s) %(levelname)s %(name)s:%(funcName)s:%(lineno)s - %(message)s"


def setup_logging(level):
    level = getattr(logging, level.upper())
    h = logging.StreamHandler()
    h.setLevel(level)
    h.setFormatter(logging.Formatter(FORMAT))
    logger.setLevel(level)
    logger.addHandler(h)

    trfh = logging.handlers.TimedRotatingFileHandler('/var/logs/algotrader.log', 'h', 1, 100)
    trfh.setLevel(level)
    trfh.setFormatter(logging.Formatter(FORMAT))
    logger.addHandler(trfh)
