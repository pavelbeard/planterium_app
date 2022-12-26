import os
import os.path as os_path
import logging
import logging.handlers as log_handlers

_format_string = "[%(asctime)s] - [%(levelname)s] - [%(filename)s].[%(module)s] {%(funcName)s:%(lineno)d: %(message)s}"


def _get_file_handler():
    logs_dir_path = os.getenv(
        "DB_API_LOGS_DIR", "D:\\Pycharm\\sobes_projects\\sobes_projects\\planterium_app\\planterium_db_api\\logs"
    )

    if not os_path.exists(logs_dir_path):
        os.mkdir(logs_dir_path)

    file_handler = log_handlers.RotatingFileHandler(
        filename=os_path.join(logs_dir_path, "planterium_db_api.log"),
        maxBytes=1024**2,
        backupCount=10
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter(_format_string))

    return file_handler


def _get_stream_handler():
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.WARNING)
    stream_handler.setFormatter(logging.Formatter(_format_string))

    return stream_handler


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)
    logger.addHandler(_get_file_handler())
    logger.addHandler(_get_stream_handler())

    return logger
