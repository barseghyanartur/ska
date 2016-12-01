__title__ = 'ska.exceptions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseException',
    'ImproperlyConfigured',
    'InvalidData'
)


class BaseException(Exception):
    """Base exception."""


class ImproperlyConfigured(BaseException):
    """Improperly configured exception.

    Raised when developer didn't configure/write the code properly.
    """


class InvalidData(BaseException):
    """Invalid data exception.

    Raised when invalid data (tumpered) is detected.
    """
