import functools
import os
import time
from datetime import datetime

import loguru
from loguru import logger

PROJECT_DIR = os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
THRESHOLD_SECONDS = 60 * 10  # 10 minutes


def init_logger(filename):
    """
    Initialises a logger using loguru, Python logging made (stupidly) simple.
    Usage instructions can be found here: https://github.com/Delgan/loguru

    Args:
        filename: Path to write logs to.

    Returns:
        A loguru logger object.
    """
    logdir = os.path.join(PROJECT_DIR, "logs")
    if not os.path.exists(logdir):
        os.makedirs(logdir)
    curr_dt = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    logfile = "{}/{}_{}.log".format(logdir, filename, curr_dt)
    logger.info("Logfile created at: {}".format(logfile))

    log_fmt = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    logger.add(logfile, backtrace=True, format=log_fmt,
               colorize=True, level="INFO")
    return logger


def timeit(f):
    """Decorator for logging the execution time of a function.
    """

    @functools.wraps(f)
    def _wrap(*args, **kwargs):
        ts = time.time()
        result = f(*args, **kwargs)
        te = time.time()
        elapsed = te - ts
        logger = _find_logger(args, kwargs)
        if logger and elapsed > THRESHOLD_SECONDS:
            logger.info("{} timeit: {:.2f} seconds".format(
                f.__name__, te - ts))
        return result

    return _wrap


def _find_logger(args, kwargs):
    """Looks for logger in one of three places:
        1) kwargs with "logger" as argument name
        2) first element in args which must be instance of loguru
        3) class attributes
    """
    if "logger" in kwargs:
        return kwargs["logger"]

    if isinstance(args[0], loguru._logger.Logger):  # check if first argument is logger
        return args[0]
    elif hasattr(args[0], "__dict__"):  # check if first arg is self (class instance)
        return args[0].__dict__.get("logger")

    return
