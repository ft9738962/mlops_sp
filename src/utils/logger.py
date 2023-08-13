import logging
from datetime import datetime

_logger_instance = None

def get_logger():
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = logging.getLogger("mlops_logger")
        _logger_instance.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s %(levelname)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            )

        ch.setFormatter(formatter)

        _logger_instance.addHandler(ch)

    return _logger_instance