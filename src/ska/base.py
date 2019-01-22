import datetime
import time

from base64 import b64encode

from six import text_type, python_2_unicode_compatible

from . import error_codes
from .defaults import SIGNATURE_LIFETIME, TIMESTAMP_FORMAT
from .helpers import sorted_urlencode

__title__ = 'ska.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'SignatureValidationResult',
    'AbstractSignature',
)

# ****************************************************************************
# ****************************************************************************
# ******************************* Signature **********************************
# ****************************************************************************
# ****************************************************************************


@python_2_unicode_compatible
class SignatureValidationResult(object):
    """
    Signature validation result container.

    If signature validation result is True, things like this would work:

    >>> res = SignatureValidationResult(result=True)
    >>> print bool(res)
    True
    >>> res = SignatureValidationResult(
    >>>     result=False,
    >>>     reason=[error_codes.INVALID_SIGNATURE,]
    >>> )
    >>> print bool(res)
    False
    """

    # __slots__ = ('result', 'reason', 'errors')

    def __init__(self, result, errors=None):
        """Constructor."""
        self.result = result
        self.errors = errors if errors else {}

    def __str__(self):
        return str(self.result)
    __repr__ = __str__

    def __bool__(self):
        return self.result
    __nonzero__ = __bool__

    @property
    def message(self):
        """Human readable message of all errors.

        :return string:
        """
        return ' '.join(map(text_type, self.errors))

    @property
    def reason(self):
        """Reason.

        For backwards compatibility. Returns list of text messages.

        :return list:
        """
        return map(text_type, self.errors)


@python_2_unicode_compatible
class AbstractSignature(object):
    """Abstract class for signature generation and validation.

    Based on symmetric keys.

    :param str signature:
    :param str auth_user:
    :param float|str valid_until:
    """

    __slots__ = ('signature', 'auth_user', 'valid_until', 'extra')

    def __init__(self, signature, auth_user, valid_until, extra=None):
        """Constructor."""
        self.signature = signature
        self.auth_user = auth_user
        self.valid_until = valid_until
        self.extra = extra if extra else {}

    def __str__(self):
        return self.signature
    __repr__ = __str__

    def __bool__(self):
        return not self.is_expired()
    __nonzero__ = __bool__

    @classmethod
    def validate_signature(cls, signature, auth_user, secret_key, valid_until,
                           extra=None, return_object=False):
        """Validates the signature.

        :param str signature:
        :param str auth_user:
        :param str secret_key:
        :param float|str valid_until: Unix timestamp.
        :param dict extra: Extra arguments to be validated.
        :param bool return_object: If set to True, an instance of
            ``SignatureValidationResult`` is returned.
        :return bool:

        :example:
        >>> Signature.validate_signature(
        >>>     'EBS6ipiqRLa6TY5vxIvZU30FpnM=',
        >>>     'user',
        >>>     'your-secret-key',
        >>>     '1377997396.0'
        >>> )
        False
        """

        if isinstance(signature, str):
            signature = signature.encode()

        if not extra:
            extra = {}

        sig = cls.generate_signature(
            auth_user=auth_user,
            secret_key=secret_key,
            valid_until=valid_until,
            extra=extra
        )

        if not return_object:
            return sig.signature == signature and not sig.is_expired()

        else:
            result = (sig.signature == signature and not sig.is_expired())
            errors = []
            if sig.signature != signature:
                errors.append(error_codes.INVALID_SIGNATURE)
            if sig.is_expired():
                errors.append(error_codes.SIGNATURE_TIMESTAMP_EXPIRED)

            return SignatureValidationResult(result, errors)

    def is_expired(self):
        """Checks if current signature is expired.

        Returns True if signature is expired and False otherwise.

        :return bool:

        :example:
        >>> # Generating the signature
        >>> sig = Signature.generate_signature('user', 'your-secret-key')
        >>> sig.is_expired()
        False
        """
        now = datetime.datetime.now()
        valid_util = self.__class__.unix_timestamp_to_date(self.valid_until)

        # Expires > now is a valid condition here.
        res = valid_util > now

        # But we actually check agains is expired, so it's the opposite.
        return not res

    @classmethod
    def get_base(cls, auth_user, timestamp, extra=None):
        """Get base string.

        Add something here so that timestamp to signature conversion is not
        that obvious.

        :param string auth_user:
        :param int timestamp:
        :param dict extra:
        """
        if not extra:
            extra = {}

        _base = [str(timestamp), auth_user]

        if extra:
            urlencoded_extra = sorted_urlencode(extra)
            if urlencoded_extra:
                _base.append(urlencoded_extra)

        return ("_".join(_base)).encode()

    @staticmethod
    def make_secret_key(secret_key):
        """The secret key how its' supposed to be used in generate signature.

        :param str secret_key:
        :return str:
        """
        return secret_key.encode()  # return b64encode(secret_key)

    @classmethod
    def make_hash(cls, auth_user, secret_key, valid_until=None, extra=None):
        """Make hash.

        You should implement this method in your signature class.

        :param str auth_user:
        :param str secret_key:
        :param float|str valid_until: Unix timestamp, valid until.
        :param dict extra: Additional variables to be added.
        :return str:
        """
        raise NotImplementedError("You should implement this method!")

    @classmethod
    def generate_signature(cls, auth_user, secret_key, valid_until=None,
                           lifetime=SIGNATURE_LIFETIME, extra=None):
        """Generates the signature.

        If timestamp is given, the signature is created using the given
        timestamp. Otherwise current time is used.

        :param str auth_user:
        :param str secret_key:
        :param float|str valid_until: Unix timestamp, valid until.
        :param int lifetime: Lifetime of the signature in seconds.
        :param dict extra: Additional variables to be added.
        :return str:

        :example:
        >>> sig = Signature.generate_signature('user', 'your-secret-key')
        EBS6ipiqRLa6TY5vxIvZU30FpnM=
        """
        if not extra:
            extra = {}

        if not valid_until:
            valid_until = time.mktime(
                (
                    datetime.datetime.now() +
                    datetime.timedelta(seconds=lifetime)
                ).timetuple()
            )
        else:
            try:
                cls.unix_timestamp_to_date(valid_until)
            except Exception:
                return None  # Something went wrong

        signature = b64encode(
            cls.make_hash(auth_user, secret_key, valid_until, extra)
        )

        return cls(signature=signature, auth_user=auth_user,
                   valid_until=valid_until, extra=extra)

    @staticmethod
    def datetime_to_timestamp(dtv):
        """Human readable datetime according to the format specified.

         Format is specified in ``TIMESTAMP_FORMAT``.

        :param datetime.datetime dtv:
        :return str:
        """
        try:
            return dtv.strftime(TIMESTAMP_FORMAT)
        except Exception:
            pass

    @staticmethod
    def datetime_to_unix_timestamp(dtv):
        """Convert ``datetime.datetime`` to Unix timestamp.

        :param datetime.datetime dtv:
        :return float: Unix timestamp.
        """
        try:
            return time.mktime(dtv.timetuple())
        except Exception:
            pass

    @classmethod
    def timestamp_to_date(cls, timestamp, fail_silently=True):
        """Converts the given timestamp to date.

        If ``fail_silently`` is set to False, raises exceptions if timestamp
        is not valid timestamp (according to the format we have specified in
        the ``TIMESTAMP_FORMAT``). Mainly used internally.

        :param str timestamp:
        :param bool fail_silently:
        :return str:
        """
        try:
            return datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT)
        except Exception as err:
            if fail_silently is not True:
                raise err
            else:
                return None

    @classmethod
    def unix_timestamp_to_date(cls, timestamp, fail_silently=True):
        """Converts the given Unix timestamp to date.
        If ``fail_silently`` is set to False, raises exceptions if timestamp
        is not valid timestamp.

        :param float|str timestamp: UNIX timestamp. Possible to parse to float.
        :param bool fail_silently:
        :return str:
        """
        try:
            return datetime.datetime.fromtimestamp(float(timestamp))
        except Exception as err:
            if fail_silently is not True:
                raise err
            else:
                return None
