__title__ = 'ska.exceptions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseException', 'ImproperlyConfigured', 'InvalidData')


class BaseException(Exception):
    """
    Base exception.
    """


class ImproperlyConfigured(BaseException):
    """
    Exception raised when developer didn't configure/write the code properly.
    """


class InvalidData(BaseException):
    """
    Raised when invalid data (tumpered) is detected.
    """
