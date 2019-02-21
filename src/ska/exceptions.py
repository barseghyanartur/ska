__title__ = 'ska.exceptions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'BaseSkaException',
    'ImproperlyConfigured',
    'InvalidData',
)


class BaseSkaException(Exception):
    """Base exception."""


class ImproperlyConfigured(BaseSkaException):
    """Improperly configured exception.

    Raised when developer didn't configure/write the code properly.
    """


class InvalidData(BaseSkaException):
    """Invalid data exception.

    Raised when invalid data (tampered) is detected.
    """
