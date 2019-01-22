from six import python_2_unicode_compatible

from .gettext import _

__title__ = 'ska.error_codes'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'ErrorCode',
    'INVALID_SIGNATURE',
    'SIGNATURE_TIMESTAMP_EXPIRED',
)


@python_2_unicode_compatible
class ErrorCode(object):
    """Base error code.

    If you have ever used the following code with `validation_result`:

    >>> human_readable_error = ' '.join(validation_result.reason)

    ...change it as follows:

    >>> human_readable_error = validation_result.message

    :property int code: Just an integer code.
    :property string message: Human readable represantation of the error
        message.
    """
    __slots__ = ('code', 'message')

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return self.message
    __repr__ = __str__

    def __int__(self):
        return self.code


INVALID_SIGNATURE = ErrorCode(1, _("Invalid signature!"))
SIGNATURE_TIMESTAMP_EXPIRED = ErrorCode(2, _("Signature timestamp expired!"))
