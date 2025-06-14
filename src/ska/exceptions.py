__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = (
    "BaseSkaException",
    "ImproperlyConfigured",
    "InvalidData",
)


class BaseSkaException(Exception):  # noqa
    """Base exception."""


class ImproperlyConfigured(BaseSkaException):
    """Improperly configured exception.

    Raised when developer didn't configure/write the code properly.
    """


class InvalidData(BaseSkaException):
    """Invalid data exception.

    Raised when invalid data (tampered) is detected.
    """
