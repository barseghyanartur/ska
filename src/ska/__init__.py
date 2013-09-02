__title__ = 'ska'
__version__ = '0.2'
__build__ = 0x000002
__author__ = 'Artur Barseghyan'
__all__ = ('Signature', 'RequestHelper', 'sign_url')

import urllib
import datetime
import time
import hmac
from base64 import b64decode, b64encode
from hashlib import sha1

from ska.defaults import SIGNATURE_LIFETIME, TIMESTAMP_FORMAT
from ska.defaults import DEFAULT_SIGNATURE_PARAM, DEFAULT_AUTH_USER_PARAM, DEFAULT_VALID_UNTIL_PARAM

_ = lambda x: x # For future integrations with gettext

class SignatureValidationResult(object):
    """
    Signature validation result container.

    If signature validation result is True, things like this would work
    >>> res = SignatureValidationResult(result=True)
    >>> print bool(res)
    True
    >>> res = SignatureValidationResult(result=False, reason=_("Invalid signature"))
    >>> print bool(res)
    False
    """
    #__slots__ = ('result', 'reason')

    def __init__(self, result, reason=[]):
        self.result = result
        self.reason = reason

    def __str__(self):
        return self.result
    __unicode__ = __str__
    __repr__ = __str__

    def __bool__(self):
        return self.result
    __nonzero__ = __bool__


class Signature(object):
    """
    Signature generation and validation based on symmetric keys.

    :param str signature:
    :param str auth_user:
    :param float|str valid_until:
    """
    __slots__ = ('signature', 'auth_user', 'valid_until')

    def __init__(self, signature, auth_user, valid_until):
        self.signature = signature
        self.auth_user = auth_user
        self.valid_until = valid_until

    def __str__(self):
        return self.signature
    __unicode__ = __str__
    __repr__ = __str__

    def __bool__(self):
        return self.result
    __nonzero__ = __bool__

    @classmethod
    def validate_signature(cls, signature, auth_user, secret_key, valid_until, return_object=False):
        """
        Validates the signature.

        :param str signature:
        :param str auth_user:
        :param str secret_key:
        :param float|str valid_until: Unix timestamp.
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
        sig = cls.generate_signature(auth_user=auth_user, secret_key=secret_key, valid_until=valid_until)

        if not return_object:
            return sig.signature == signature and not sig.is_expired()

        else:
            result = (sig.signature == signature and not sig.is_expired())
            reason = []
            if sig.signature != signature:
                reason.append(_("Invalid signature!"))
            if sig.is_expired():
                reason.append(_("Signature timestamp expired!"))

            return SignatureValidationResult(result, reason)

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
        valid_util = Signature.unix_timestamp_to_date(self.valid_until)

        # Expires > now is a valid condition here.
        res = valid_util > now

        # But we actually check agains is expired, so it's the opposite.
        return not res

    @classmethod
    def get_base(cls, auth_user, timestamp):
        """
        Add something here so that timestamp to signature conversion is not that obvious.
        """
        l = [str(timestamp), auth_user]

        return "_".join(l)

    @staticmethod
    def make_secret_key(secret_key):
        """
        The secret key how its' supposed to be used in generate signature.

        :param str secret_key:
        :return str:
        """
        return secret_key #return b64encode(secret_key)

    @classmethod
    def generate_signature(cls, auth_user, secret_key, valid_until=None, lifetime=SIGNATURE_LIFETIME):
        """
        Generates the signature. If timestamp is given, the signature is created using the given timestamp. Otherwise
        current time is used.

        :param str auth_user:
        :param str secret_key:
        :param float|str valid_until: Unix timestamp, valid until.
        :param int lifetime: Lifetime of the signature in seconds.
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

        raw_hmac = hmac.new(Signature.make_secret_key(secret_key), cls.get_base(auth_user, valid_until), sha1).digest()
        signature = b64encode(raw_hmac)
        return Signature(signature=signature, auth_user=auth_user, valid_until=valid_until)

    @staticmethod
    def datetime_to_timestamp(dt):
        """
        Human readable datetime according to the format specified in ``TIMESTAMP_FORMAT``.

        :param datetime.datetime dt:
        :return str:
        """
        try:
            return dt.strftime(TIMESTAMP_FORMAT)
        except Exception, e:
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
        except Exception, e:
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


class RequestHelper(object):
    """
    Request helper for easy put/extract of signature params from URLs.
    """
    def __init__(self, signature_param, auth_user_param, valid_until_param):
        self.signature_param = signature_param
        self.auth_user_param = auth_user_param
        self.valid_until_param = valid_until_param

    def signature_to_url(self, signature, endpoint_url=''):
        """
        URL encodes the signature params.

        :param ska.Signature signature:
        :param str endpoint_url:
        :return str:

        :example:

        Required imports.

        >>> from ska import Signature, RequestHelper

        Generate signature.

        >>> signature = Signature.generate_signature(
        >>>     auth_user = 'user',
        >>>     secret_key = 'your-secret-key'
        >>>     )

        Create a request helper.

        >>> request_helper = RequestHelper(
        >>>     signature_param = 'signature',
        >>>     auth_user_param = 'auth_user',
        >>>     valid_until_param = 'valid_until'
        >>> )

        Appending signature params to the endpoint URL.

        >>> url = request_helper.signature_to_url(
        >>>     signature = signature,
        >>>     endpoint_url = 'http://e.com/api/'
        >>> )
        http://e.com/api/?valid_until=1378045287.0&auth_user=user&signature=YlZpLFsjUKBalL4x5trhkeEgqE8%3D
        """
        params = {
            self.signature_param: signature.signature,
            self.auth_user_param: signature.auth_user,
            self.valid_until_param: signature.valid_until,
        }
        return "%s?%s" % (endpoint_url, urllib.urlencode(params))

    def validate_request_data(self, data, secret_key):
        """
        Validates the request data.
        
        :param dict data:
        :param str secret_key:
        :return ska.SignatureValidationResult:

        :example:
        If your imaginary ``HttpRequest`` object has ``GET`` property (dict), then you
        would validate the request data as follows.

        Create a ``RequestHelper`` object with param names expected.

        Required imports.

        >>> from ska import RequestHelper

        Create a request helper.

        >>> request_helper = RequestHelper(
        >>>     signature_param = 'signature',
        >>>     auth_user_param = 'auth_user',
        >>>     valid_until_param = 'valid_until'
        >>> )

        Validate the request data.
        
        >>> validation_result = request_helper.validate_request_data(
        >>>     data = request.GET,
        >>>     secret_key = 'your-secret-key'
        >>> )
        """
        signature = data.get(self.signature_param, '')
        auth_user = data.get(self.auth_user_param, '')
        valid_until = data.get(self.valid_until_param, '')

        validation_result = Signature.validate_signature(
            signature = signature,
            auth_user = auth_user,
            secret_key = secret_key,
            valid_until = valid_until,
            return_object = True
            )

        return validation_result

def sign_url(auth_user, secret_key, valid_until=None, lifetime=SIGNATURE_LIFETIME, url='', \
             signature_param='signature', auth_user_param='auth_user', \
             valid_until_param='valid_until'):
    """
    Signs the URL.

    :param str auth_user: Username of the user making the request.
    :param str secret_key: The shared secret key.
    :param float|str valid_until: Unix timestamp. If not given, generated automatically (now + lifetime).
    :param int lifetime: Signature lifetime in seconds.
    :param str url: URL to be signed.
    :param str signature_param: Name of the GET param name which would hold the generated signature value.
    :param str auth_user_param: Name of the GET param name which would hold the ``auth_user`` value.
    :param str valid_until_param: Name of the GET param name which would hold the ``valid_until`` value.
    :return str:

    :example:
    Required imports.

    >>> from ska import sign_url

    Producing a signed URL.

    >>> signed_url = sign_url(
    >>>     auth_user='user', secret_key='your-secret_key', lifetime=120, \
    >>>     url='http://e.com/api/', signature_param=DEFAULT_SIGNATURE_PARAM,
    >>>     auth_user_param=DEFAULT_AUTH_USER_PARAM, valid_until_param=DEFAULT_VALID_UNTIL_PARAM
    >>> )
    http://e.com/api/?valid_until=1378045287.0&auth_user=user&signature=YlZpLFsjUKBalL4x5trhkeEgqE8%3D
    """
    if lifetime is None:
        lifetime=SIGNATURE_LIFETIME

    assert isinstance(lifetime, int)

    signature = Signature.generate_signature(
        auth_user = auth_user,
        secret_key = secret_key,
        valid_until = valid_until,
        lifetime = lifetime
        )

    request_helper = RequestHelper(
        signature_param = signature_param,
        auth_user_param = auth_user_param,
        valid_until_param = valid_until_param
    )

    signed_url = request_helper.signature_to_url(
        signature = signature,
        endpoint_url = url
    )

    return signed_url

def validate_signed_request_data(data, secret_key, signature_param=DEFAULT_SIGNATURE_PARAM, \
                                 auth_user_param=DEFAULT_AUTH_USER_PARAM, \
                                 valid_until_param=DEFAULT_VALID_UNTIL_PARAM):
    """
    Validates the signed request data.

    :param dict data: Dictionary holding the HTTP request GET data.
    :param str secret_key: The shared secret key.
    :param str signature_param: Name of the GET param name which holds the signature value.
    :param str auth_user_param: Name of the GET param name which holds the ``auth_user`` value.
    :param str valid_until_param: Name of the GET param name which holds the ``valid_until`` value.
    :return ska.SignatureValidationResult: A ``ska.SignatureValidationResult`` object with the
        following properties:
            - `result` (bool): True if data is valid. False otherwise.
            - `reason` (list): List of strings, indicating validation errors. Empty list in case
              if `result` is True.
    """
    request_helper = RequestHelper(
        signature_param = signature_param,
        auth_user_param = auth_user_param,
        valid_until_param = valid_until_param
    )

    validation_result = request_helper.validate_request_data(
        data = data,
        secret_key = secret_key
    )

    return validation_result
