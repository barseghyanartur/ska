__title__ = 'ska.base'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'SignatureValidationResult', 'AbstractSignature',
    )

import datetime
import time
from base64 import b64encode

from six import text_type

from ska import error_codes
from ska.helpers import sorted_urlencode
from ska.defaults import (
    SIGNATURE_LIFETIME, TIMESTAMP_FORMAT,
    )

_ = lambda x: x # For future integrations with gettext

# *******************************************************************************************************
# *******************************************************************************************************
# ******************************************* Signature *************************************************
# *******************************************************************************************************
# *******************************************************************************************************

class SignatureValidationResult(object):
    """
    Signature validation result container.

    If signature validation result is True, things like this would work:

    >>> res = SignatureValidationResult(result=True)
    >>> print bool(res)
    True
    >>> res = SignatureValidationResult(result=False, reason=[error_codes.INVALID_SIGNATURE,])
    >>> print bool(res)
    False
    """
    #__slots__ = ('result', 'reason', 'errors')

    def __init__(self, result, errors=[]):
        self.result = result
        self.errors = errors

    def __str__(self):
        return str(self.result)
    __unicode__ = __str__
    __repr__ = __str__

    def __bool__(self):
        return self.result
    __nonzero__ = __bool__

    @property
    def message(self):
        """
        Human readable message of all errors.

        :return string:
        """
        return ' '.join(map(text_type, self.errors))

    @property
    def reason(self):
        """
        For backwards compatibility. Returns list of text messages.

        :return list:
        """
        return map(text_type, self.errors)


class AbstractSignature(object):
    """
    Abstract class for signature generation and validation based on symmetric keys.

    :param str signature:
    :param str auth_user:
    :param float|str valid_until:
    """
    __slots__ = ('signature', 'auth_user', 'valid_until', 'extra')

    def __init__(self, signature, auth_user, valid_until, extra={}):
        self.signature = signature
        self.auth_user = auth_user
        self.valid_until = valid_until
        self.extra = extra

    def __str__(self):
        return self.signature
    __unicode__ = __str__
    __repr__ = __str__

    def __bool__(self):
        return self.result
    __nonzero__ = __bool__

    @classmethod
    def validate_signature(cls, signature, auth_user, secret_key, valid_until, extra={}, return_object=False):
        """
        Validates the signature.

        :param str signature:
        :param str auth_user:
        :param str secret_key:
        :param float|str valid_until: Unix timestamp.
        :param dict extra: Extra arguments to be validated.
        :param bool return_object: If set to True, an instance of ``SignatureValidationResult`` is returned.
        :return bool:

        :example:
        >>> Signature.validate_signature(
            'EBS6ipiqRLa6TY5vxIvZU30FpnM=',
            'user',
            'your-secret-key',
            '1377997396.0'
            )
        False
        """
        if isinstance(signature, str):
            signature = signature.encode()

        sig = cls.generate_signature(
            auth_user = auth_user,
            secret_key = secret_key,
            valid_until = valid_until,
            extra = extra
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
        """
        Checks if current signature is expired. Returns True if signature is expired and False otherwise.

        :return bool:

        :example:
        >>> sig = Signature.generate_signature('user', 'your-secret-key') # Generating the signature
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
    def get_base(cls, auth_user, timestamp, extra={}):
        """
        Add something here so that timestamp to signature conversion is not that obvious.

        :param string auth_user:
        :param int timestamp:
        :param dict extra:
        """
        l = [str(timestamp), auth_user]

        if extra:
            urlencoded_extra = sorted_urlencode(extra)
            if urlencoded_extra:
                l.append(urlencoded_extra)

        return ("_".join(l)).encode()

    @staticmethod
    def make_secret_key(secret_key):
        """
        The secret key how its' supposed to be used in generate signature.

        :param str secret_key:
        :return str:
        """
        return secret_key.encode() #return b64encode(secret_key)

    @classmethod
    def make_hash(cls, auth_user, secret_key, valid_until=None, extra={}):
        """
        You should implement this method in your signature class.

        :param str auth_user:
        :param str secret_key:
        :param float|str valid_until: Unix timestamp, valid until.
        :param dict extra: Additional variables to be added.
        :return str:
        """
        raise NotImplemented("You should implement this method!")

    @classmethod
    def generate_signature(cls, auth_user, secret_key, valid_until=None, lifetime=SIGNATURE_LIFETIME, extra={}):
        """
        Generates the signature. If timestamp is given, the signature is created using the given timestamp. Otherwise
        current time is used.

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
        if not valid_until:
            valid_until = time.mktime(
                (datetime.datetime.now() + datetime.timedelta(seconds=lifetime)).timetuple()
                )
        else:
            try:
                cls.unix_timestamp_to_date(valid_until)
            except Exception as e:
                return None # Something went wrong

        signature = b64encode(cls.make_hash(auth_user, secret_key, valid_until, extra))

        return cls(signature=signature, auth_user=auth_user, valid_until=valid_until, extra=extra)

    @staticmethod
    def datetime_to_timestamp(dt):
        """
        Human readable datetime according to the format specified in ``TIMESTAMP_FORMAT``.

        :param datetime.datetime dt:
        :return str:
        """
        try:
            return dt.strftime(TIMESTAMP_FORMAT)
        except Exception as e:
            pass

    @staticmethod
    def datetime_to_unix_timestamp(dt):
        """
        Converts ``datetime.datetime`` to Unix timestamp.

        :param datetime.datetime dt:
        :return float: Unix timestamp.
        """
        try:
            return time.mktime(dt.timetuple())
        except Exception as e:
            pass

    @classmethod
    def timestamp_to_date(cls, timestamp, fail_silently=True):
        """
        Converts the given timestamp to date. If ``fail_silently`` is set to False, raises
        exceptions if timestamp is not valid timestamp (according to the format we have
        specified in the ``TIMESTAMP_FORMAT``). Mainly used internally.

        :param str timestamp:
        :param bool fail_silently:
        :return str:
        """
        try:
            return datetime.datetime.strptime(timestamp, TIMESTAMP_FORMAT)
        except Exception as e:
            if fail_silently is not True:
                raise e
            else:
                return None

    @classmethod
    def unix_timestamp_to_date(cls, timestamp, fail_silently=True):
        """
        Converts the given Unix timestamp to date. If ``fail_silently`` is set to False, raises
        exceptions if timestamp is not valid timestamp.

        :param float|str timestamp: UNIX timestamp. Parsable to float.
        :param bool fail_silently:
        :return str:
        """
        try:
            return datetime.datetime.fromtimestamp(float(timestamp))
        except Exception as e:
            if fail_silently is not True:
                raise e
            else:
                return None
