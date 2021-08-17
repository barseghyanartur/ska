from typing import Dict, Optional, Type, Union, Callable

from .base import SignatureValidationResult, AbstractSignature
from .defaults import (
    DEFAULT_AUTH_USER_PARAM,
    DEFAULT_EXTRA_PARAM,
    DEFAULT_SIGNATURE_PARAM,
    DEFAULT_URL_SUFFIX,
    DEFAULT_VALID_UNTIL_PARAM,
    SIGNATURE_LIFETIME,
)
from .signatures import Signature
from .utils import RequestHelper

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = (
    "extract_signed_request_data",
    "sign_url",
    "signature_to_dict",
    "validate_signed_request_data",
)


# **************************************************************************
# **************************************************************************
# ************************** Shortcut functions ****************************
# **************************************************************************
# **************************************************************************


def sign_url(
    auth_user: str,
    secret_key: str,
    valid_until: Optional[Union[float, str]] = None,
    lifetime: int = SIGNATURE_LIFETIME,
    url: str = "",
    suffix: str = DEFAULT_URL_SUFFIX,
    signature_param: str = DEFAULT_SIGNATURE_PARAM,
    auth_user_param: str = DEFAULT_AUTH_USER_PARAM,
    valid_until_param: str = DEFAULT_VALID_UNTIL_PARAM,
    extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
    extra_param: str = DEFAULT_EXTRA_PARAM,
    signature_cls: Type[AbstractSignature] = Signature,
    value_dumper: Optional[Callable] = None,
) -> str:
    """Sign the URL.

    :param auth_user: Username of the user making the request.
    :param secret_key: The shared secret key.
    :param valid_until: Unix timestamp. If not given, generated
        automatically (now + lifetime).
    :param lifetime: Signature lifetime in seconds.
    :param url: URL to be signed.
    :param suffix: Suffix to add after the ``endpoint_url`` and before
        the appended signature params.
    :param signature_param: Name of the GET param name which would hold
        the generated signature value.
    :param auth_user_param: Name of the GET param name which would hold
        the ``auth_user`` value.
    :param valid_until_param: Name of the GET param name which would
        hold the ``valid_until`` value.
    :param extra: Extra variables to add to the request.
    :param extra_param: Name of the GET param name which would hold the
        ``extra_keys`` value.
    :param signature_cls:
    :param value_dumper:
    :return:

    :example:
    Required imports.

    >>> from ska import sign_url

    Producing a signed URL.

    >>> signed_url = sign_url(
    >>>     auth_user='user', secret_key='your-secret_key', lifetime=120,
    >>>     url='http://e.com/api/', signature_param=DEFAULT_SIGNATURE_PARAM,
    >>>     auth_user_param=DEFAULT_AUTH_USER_PARAM,
    >>>     valid_until_param=DEFAULT_VALID_UNTIL_PARAM,
    >>>     extra={
    >>>         'provider': 'service1.example.com',
    >>>         'email': 'john.doe@mail.example.com'
    >>>     },
    >>>     extra_param = DEFAULT_EXTRA_PARAM
    >>> )
    http://e.com/api/?valid_until=1378045287.0&auth_user=user&signature=
    YlZpLFsjUKBalL4x5trhkeEgqE8%3D
    """
    if lifetime is None:
        lifetime = SIGNATURE_LIFETIME

    if not extra:
        extra = {}

    assert isinstance(lifetime, int)

    signature = signature_cls.generate_signature(
        auth_user=auth_user,
        secret_key=secret_key,
        valid_until=valid_until,
        lifetime=lifetime,
        extra=extra,
        value_dumper=value_dumper,
    )

    request_helper = RequestHelper(
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra_param=extra_param,
        signature_cls=signature_cls,
    )

    signed_url = request_helper.signature_to_url(
        signature=signature,
        endpoint_url=url,
        suffix=suffix,
    )

    return signed_url


def signature_to_dict(
    auth_user: str,
    secret_key: str,
    valid_until: Optional[Union[float, str]] = None,
    lifetime: int = SIGNATURE_LIFETIME,
    signature_param: str = DEFAULT_SIGNATURE_PARAM,
    auth_user_param: str = DEFAULT_AUTH_USER_PARAM,
    valid_until_param: str = DEFAULT_VALID_UNTIL_PARAM,
    extra: Optional[Dict[str, Union[str, int]]] = None,
    extra_param: str = DEFAULT_EXTRA_PARAM,
    signature_cls: Type[AbstractSignature] = Signature,
    value_dumper: Optional[Callable] = None,
    quoter: Optional[Callable] = None,
) -> Dict[str, Union[bytes, str, float, int]]:
    """Return a dictionary containing the signature data params.

    :param auth_user: Username of the user making the request.
    :param secret_key: The shared secret key.
    :param valid_until: Unix timestamp. If not given, generated
        automatically (now + lifetime).
    :param lifetime: Signature lifetime in seconds.
    :param signature_param: Name of the (for example POST) param name
        which would hold the generated ``signature`` value.
    :param auth_user_param: Name of the (for example POST) param name
        which would hold the ``auth_user`` value.
    :param valid_until_param: Name of the (for example POST) param name
        which would hold the ``valid_until`` value.
    :param extra: Additional arguments for the signature.
    :param extra_param: Name of the (for example POST) param name which
        would hold the ``extra`` keys value.
    :param signature_cls:
    :param value_dumper:
    :param quoter:
    :return:

    :example:
    Required imports.

    >>> from ska import signature_to_dict

    Producing a dictionary with signature data.

    >>> signature_dict = signature_to_dict(
    >>>     auth_user='user', secret_key='your-secret_key', lifetime=120,
    >>>     signature_param=DEFAULT_SIGNATURE_PARAM,
    >>>     auth_user_param=DEFAULT_AUTH_USER_PARAM,
    >>>     valid_until_param=DEFAULT_VALID_UNTIL_PARAM
    >>> )
    {
        'signature': 'YlZpLFsjUKBalL4x5trhkeEgqE8=',
        'auth_user': 'user',
        'valid_until': '1378045287.0'
    }
    """
    if lifetime is None:
        lifetime = SIGNATURE_LIFETIME

    if not extra:
        extra = {}

    assert isinstance(lifetime, int)

    signature = signature_cls.generate_signature(
        auth_user=auth_user,
        secret_key=secret_key,
        valid_until=valid_until,
        lifetime=lifetime,
        extra=extra,
        value_dumper=value_dumper,
        quoter=quoter,
    )

    request_helper = RequestHelper(
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra_param=extra_param,
        signature_cls=signature_cls,
    )

    signature_dict = request_helper.signature_to_dict(signature=signature)

    return signature_dict


def validate_signed_request_data(
    data: Dict[str, Union[bytes, str, float, int]],
    secret_key: str,
    signature_param: str = DEFAULT_SIGNATURE_PARAM,
    auth_user_param: str = DEFAULT_AUTH_USER_PARAM,
    valid_until_param: str = DEFAULT_VALID_UNTIL_PARAM,
    extra_param: str = DEFAULT_EXTRA_PARAM,
    signature_cls: Type[AbstractSignature] = Signature,
    value_dumper: Optional[Callable] = None,
    quoter: Optional[Callable] = None,
) -> SignatureValidationResult:
    """Validate the signed request data.

    :param data: Dictionary holding the (HTTP) request (for example GET
        or POST) data.
    :param secret_key: The shared secret key.
    :param signature_param: Name of the (for example GET or POST) param
        name which holds the ``signature`` value.
    :param auth_user_param: Name of the (for example GET or POST) param
        name which holds the ``auth_user`` value.
    :param valid_until_param: Name of the (foe example GET or POST)
        param name which holds the ``valid_until`` value.
    :param extra_param: Name of the (foe example GET or POST) param
        name which holds the ``extra`` keys value.
    :param signature_cls:
    :param value_dumper:
    :param quoter:
    :return: A ``ska.SignatureValidationResult``
        object with the following properties:
            - `result` (bool): True if data is valid. False otherwise.
            - `reason` (Iterable): List of strings, indicating validation
              errors. Empty list in case if `result` is True.
    """
    request_helper = RequestHelper(
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra_param=extra_param,
        signature_cls=signature_cls,
    )

    validation_result = request_helper.validate_request_data(
        data=data,
        secret_key=secret_key,
        value_dumper=value_dumper,
        quoter=quoter,
    )

    return validation_result


def extract_signed_request_data(
    data: Dict[str, Union[bytes, str, float, int]],
    secret_key: Optional[str] = None,
    signature_param: str = DEFAULT_SIGNATURE_PARAM,
    auth_user_param: str = DEFAULT_AUTH_USER_PARAM,
    valid_until_param: str = DEFAULT_VALID_UNTIL_PARAM,
    extra_param: str = DEFAULT_EXTRA_PARAM,
    validate: bool = False,
    fail_silently: bool = False,
    signature_cls: Type[AbstractSignature] = Signature,
    value_dumper: Optional[Callable] = None,
    quoter: Optional[Callable] = None,
) -> Dict[str, Union[bytes, str, float, int]]:
    """Validate the signed request data.

    :param data: Dictionary holding the (HTTP) request (for example
        GET or POST) data.
    :param secret_key: The shared secret key.
    :param signature_param: Name of the (for example GET or POST) param
        name which holds the ``signature`` value.
    :param auth_user_param: Name of the (for example GET or POST) param
        name which holds the ``auth_user`` value.
    :param valid_until_param: Name of the (foe example GET or POST) param
        name which holds the ``valid_until`` value.
    :param extra_param: Name of the (foe example GET or POST) param name
        which holds the ``extra`` value.
    :param validate: If set to True, request data is validated before
        returning the result.
    :param fail_silently: If set to True, exceptions are omitted.
    :param signature_cls:
    :param value_dumper:
    :param quoter:
    :return: Dictionary with signed request data.
    """
    request_helper = RequestHelper(
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra_param=extra_param,
        signature_cls=signature_cls,
    )

    return request_helper.extract_signed_data(
        data,
        secret_key=secret_key,
        validate=validate,
        fail_silently=fail_silently,
        value_dumper=value_dumper,
        quoter=quoter,
    )
