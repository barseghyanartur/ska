import datetime
import logging
from urllib.parse import urlparse, parse_qs

from .. import TIMESTAMP_FORMAT

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = (
    "LOG_INFO",
    "log_info",
    "timestamp_to_human_readable",
    "parse_url_params",
)


logger = logging.getLogger(__name__)
LOG_INFO = True


def log_info(func):
    """Prints some useful info."""
    if not LOG_INFO:
        return func

    def inner(self, *args, **kwargs):
        """Inner"""
        result = func(self, *args, **kwargs)

        logger.debug(f"\n\n{func.__name__}")
        logger.debug("============================")
        if func.__doc__:
            logger.debug(f'""" {func.__doc__.strip()} """')
        logger.debug("----------------------------")
        if result is not None:
            logger.debug(result)
        logger.debug("\n++++++++++++++++++++++++++++")

        return result

    return inner


def timestamp_to_human_readable(timestamp):
    """Convert Unix timestamp to human readable string.

    :param timestamp:
    :return str:
    """
    val = datetime.datetime.fromtimestamp(float(timestamp))
    return val.strftime(TIMESTAMP_FORMAT)


def parse_url_params(url):
    """Parses URL params.

    :param str url:
    :return dict:
    """
    data = parse_qs(urlparse(url).query)
    for key, val in data.items():
        data[key] = val[0]

    return data
