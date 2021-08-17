from base64 import b64encode
from datetime import datetime, timedelta
import time
from typing import Any, Dict, List, Optional, Union, Callable

from . import error_codes
from .defaults import SIGNATURE_LIFETIME, TIMESTAMP_FORMAT
from .error_codes import ErrorCode
from .helpers import sorted_urlencode

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = (
    "SignatureValidationResult",
    "AbstractSignature",
)

# ****************************************************************************
# ****************************************************************************
# ******************************* Signature **********************************
# ****************************************************************************
# ****************************************************************************


class SignatureValidationResult:
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

    def __init__(
        self,
        result: bool,
        errors: Optional[List[Union[ErrorCode, Any]]] = None,
    ) -> None:
        """Constructor."""
        self.result = result
        self.errors = errors if errors else {}

    def __str__(self) -> str:
        return str(self.result)

    __repr__ = __str__

    def __bool__(self) -> bool:
        return self.result

    __nonzero__ = __bool__

    @property
    def message(self) -> str:
        """Human readable message of all errors.

        :return:
        """
        return " ".join(map(str, self.errors))

    @property
    def reason(self) -> map:
        """Reason.

        For backwards compatibility. Returns list of text messages.

        :return:
        """
        return map(str, self.errors)


class AbstractSignature:
    """Abstract class for signature generation and validation.

    Based on symmetric keys.

    :param signature:
    :param auth_user:
    :param valid_until:
    """

    __slots__ = (
        "signature",
        "auth_user",
        "valid_until",
        "extra",
    )

    def __init__(
        self,
        signature: bytes,
        auth_user: str,
        valid_until: Union[float, str],
        extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
    ) -> None:
        """Constructor."""
        self.signature = signature
        self.auth_user = auth_user
        self.valid_until = valid_until
        self.extra = extra if extra else {}

    def __str__(self) -> str:
        return self.signature.decode()

    __repr__ = __str__

    def __bool__(self) -> bool:
        return not self.is_expired()

    __nonzero__ = __bool__

    @classmethod
    def validate_signature(
        cls,
        signature: Union[str, bytes],
        auth_user: str,
        secret_key: str,
        valid_until: Union[str, float],
        extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
        return_object: bool = False,
        value_dumper: Optional[Callable] = None,
        quoter: Optional[Callable] = None,
    ) -> Union[SignatureValidationResult, bool]:
        """Validates the signature.

        :param signature:
        :param auth_user:
        :param secret_key:
        :param valid_until: Unix timestamp.
        :param extra: Extra arguments to be validated.
        :param return_object: If set to True, an instance of
            ``SignatureValidationResult`` is returned.
        :param value_dumper:
        :param quoter:
        :return:

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
            extra=extra,
            value_dumper=value_dumper,
            quoter=quoter,
        )

        if not return_object:
            return sig.signature == signature and not sig.is_expired()

        else:
            result = sig.signature == signature and not sig.is_expired()
            errors = []
            if sig.signature != signature:
                errors.append(error_codes.INVALID_SIGNATURE)
            if sig.is_expired():
                errors.append(error_codes.SIGNATURE_TIMESTAMP_EXPIRED)

            return SignatureValidationResult(result, errors)

    def is_expired(self) -> bool:
        """Checks if current signature is expired.

        Returns True if signature is expired and False otherwise.

        :return:

        :example:
        >>> # Generating the signature
        >>> sig = Signature.generate_signature('user', 'your-secret-key')
        >>> sig.is_expired()
        False
        """
        now = datetime.now()
        valid_util = self.__class__.unix_timestamp_to_date(self.valid_until)

        # Expires > now is a valid condition here.
        res = valid_util > now

        # But we actually check agains is expired, so it's the opposite.
        return not res

    @classmethod
    def get_base(
        cls,
        auth_user: str,
        timestamp: Union[float, str],
        extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
        value_dumper: Optional[Callable] = None,
        quoter: Optional[Callable] = None,
    ) -> bytes:
        """Get base string.

        Add something here so that timestamp to signature conversion is not
        that obvious.

        :param auth_user:
        :param timestamp:
        :param extra:
        :param value_dumper:
        :param quoter:
        """
        if not extra:
            extra = {}

        _base = [str(timestamp), auth_user]

        if extra:
            urlencoded_extra = sorted_urlencode(
                extra,
                value_dumper=value_dumper,
                quoter=quoter,
            )
            if urlencoded_extra:
                _base.append(urlencoded_extra)

        return ("_".join(_base)).encode()

    @staticmethod
    def make_secret_key(secret_key: str) -> bytes:
        """The secret key how its' supposed to be used in generate signature.

        :param secret_key:
        :return:
        """
        return secret_key.encode()  # return b64encode(secret_key)

    @classmethod
    def make_hash(
        cls,
        auth_user: str,
        secret_key: str,
        valid_until: Union[str, float] = None,
        extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
        value_dumper: Optional[Callable] = None,
        quoter: Optional[Callable] = None,
    ) -> bytes:
        """Make hash.

        You should implement this method in your signature class.

        :param auth_user:
        :param secret_key:
        :param valid_until: Unix timestamp, valid until.
        :param extra: Additional variables to be added.
        :param value_dumper:
        :param quoter:
        :return:
        """
        raise NotImplementedError("You should implement this method!")

    @classmethod
    def generate_signature(
        cls,
        auth_user: str,
        secret_key: str,
        valid_until: Optional[Union[float, str]] = None,
        lifetime: int = SIGNATURE_LIFETIME,
        extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
        value_dumper: Optional[Callable] = None,
        quoter: Optional[Callable] = None,
    ) -> "AbstractSignature":
        """Generates the signature.

        If timestamp is given, the signature is created using the given
        timestamp. Otherwise current time is used.

        :param auth_user:
        :param secret_key:
        :param valid_until: Unix timestamp, valid until.
        :param lifetime: Lifetime of the signature in seconds.
        :param extra: Additional variables to be added.
        :param value_dumper:
        :param quoter:
        :return:

        :example:
        >>> sig = Signature.generate_signature('user', 'your-secret-key')
        EBS6ipiqRLa6TY5vxIvZU30FpnM=
        """
        if not extra:
            extra = {}

        if not valid_until:
            valid_until = time.mktime(
                (datetime.now() + timedelta(seconds=lifetime)).timetuple()
            )
        else:
            try:
                cls.unix_timestamp_to_date(valid_until)
            except Exception:
                return None  # Something went wrong

        signature = b64encode(
            cls.make_hash(
                auth_user,
                secret_key,
                valid_until,
                extra,
                value_dumper=value_dumper,
                quoter=quoter,
            )
        )

        return cls(
            signature=signature,
            auth_user=auth_user,
            valid_until=valid_until,
            extra=extra,
        )

    @staticmethod
    def datetime_to_timestamp(dtv: datetime) -> Optional[str]:
        """Human readable datetime according to the format specified.

         Format is specified in ``TIMESTAMP_FORMAT``.

        :param dtv:
        :return:
        """
        try:
            return dtv.strftime(TIMESTAMP_FORMAT)
        except Exception:
            pass

    @staticmethod
    def datetime_to_unix_timestamp(dtv: datetime) -> Optional[float]:
        """Convert ``datetime.datetime`` to Unix timestamp.

        :param dtv:
        :return: Unix timestamp.
        """
        try:
            return time.mktime(dtv.timetuple())
        except Exception:
            pass

    @classmethod
    def timestamp_to_date(
        cls, timestamp: Union[float, str], fail_silently: bool = True
    ) -> Union[datetime, None]:
        """Converts the given timestamp to date.

        If ``fail_silently`` is set to False, raises exceptions if timestamp
        is not valid timestamp (according to the format we have specified in
        the ``TIMESTAMP_FORMAT``). Mainly used internally.

        :param timestamp:
        :param fail_silently:
        :return:
        """
        try:
            return datetime.strptime(timestamp, TIMESTAMP_FORMAT)
        except Exception as err:
            if fail_silently is not True:
                raise err
            else:
                return None

    @classmethod
    def unix_timestamp_to_date(
        cls, timestamp: Union[float, str], fail_silently: bool = True
    ) -> Union[datetime, None]:
        """Converts the given Unix timestamp to date.
        If ``fail_silently`` is set to False, raises exceptions if timestamp
        is not valid timestamp.

        :param timestamp: UNIX timestamp. Possible to parse to float.
        :param fail_silently:
        :return:
        """
        try:
            return datetime.fromtimestamp(float(timestamp))
        except Exception as err:
            if fail_silently is not True:
                raise err
            else:
                return None
