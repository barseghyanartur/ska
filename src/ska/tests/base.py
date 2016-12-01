import datetime

from six import PY3

from .. import TIMESTAMP_FORMAT

try:
    from six.moves.urllib.parse import urlparse, parse_qs
except ImportError as err:
    if PY3:
        from urllib.parse import urlparse, parse_qs
    else:
        from urlparse import urlparse, parse_qs

__title__ = 'ska.tests.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'LOG_INFO',
    'log_info',
    'timestap_to_human_readable',
    'parse_url_params',
)


LOG_INFO = True


def log_info(func):
    """Prints some useful info."""
    if not LOG_INFO:
        return func

    def inner(self, *args, **kwargs):
        """Inner"""
        result = func(self, *args, **kwargs)

        print('\n\n%s' % func.__name__)
        print('============================')
        if func.__doc__:
            print('""" %s """' % func.__doc__.strip())
        print('----------------------------')
        if result is not None:
            print(result)
        print('\n++++++++++++++++++++++++++++')

        return result
    return inner


def timestap_to_human_readable(timestamp):
    """Convert Unix timestamp to human readable string.

    :param float:
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
