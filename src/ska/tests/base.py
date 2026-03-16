import datetime
import logging
from urllib.parse import parse_qs, urlparse

from .. import TIMESTAMP_FORMAT

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = (
    "parse_url_params",
    "timestamp_to_human_readable",
)


logger = logging.getLogger(__name__)


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
