import logging
import os
import os.path as os_path
from logging import handlers
from .startup import Startup

_logging_format = "[%(asctime)s] loglevel=%(levelname)-6s logger=%(name)s %(funcName)s() L%(lineno)-4d %(message)s"


def get_file_handler():
    logs_dir_path = Startup.get_config().get('settings').get('logs_dir_path')

    if not os_path.exists(logs_dir_path):
        os.mkdir(logs_dir_path)

    fh = logging.handlers.RotatingFileHandler(
        os.path.join(logs_dir_path, "planterium_bot.log"), backupCount=10,
        maxBytes=1024 ** 2
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter(_logging_format))
    return fh


def get_stream_handler():
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(logging.Formatter(_logging_format))
    return sh


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(get_file_handler())
    logger.addHandler(get_stream_handler())
    return logger
