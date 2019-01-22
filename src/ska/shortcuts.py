from .defaults import (
    SIGNATURE_LIFETIME,
    DEFAULT_URL_SUFFIX,
    DEFAULT_SIGNATURE_PARAM,
    DEFAULT_AUTH_USER_PARAM,
    DEFAULT_VALID_UNTIL_PARAM,
    DEFAULT_EXTRA_PARAM
)
from .signatures import Signature
from .utils import RequestHelper


__title__ = 'ska.shortcuts'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'extract_signed_request_data',
    'sign_url',
    'signature_to_dict',
    'validate_signed_request_data',
)


# **************************************************************************
# **************************************************************************
# ************************** Shortcut functions ****************************
# **************************************************************************
# **************************************************************************


def sign_url(auth_user,
             secret_key,
             valid_until=None,
             lifetime=SIGNATURE_LIFETIME,
             url='',
             suffix=DEFAULT_URL_SUFFIX,
             signature_param=DEFAULT_SIGNATURE_PARAM,
             auth_user_param=DEFAULT_AUTH_USER_PARAM,
             valid_until_param=DEFAULT_VALID_UNTIL_PARAM,
             extra=None,
             extra_param=DEFAULT_EXTRA_PARAM,
             signature_cls=Signature):
    """Sign the URL.

    :param str auth_user: Username of the user making the request.
    :param str secret_key: The shared secret key.
    :param float|str valid_until: Unix timestamp. If not given, generated
        automatically (now + lifetime).
    :param int lifetime: Signature lifetime in seconds.
    :param str url: URL to be signed.
    :param str suffix: Suffix to add after the ``endpoint_url`` and before
        the appended signature params.
    :param str signature_param: Name of the GET param name which would hold
        the generated signature value.
    :param str auth_user_param: Name of the GET param name which would hold
        the ``auth_user`` value.
    :param str valid_until_param: Name of the GET param name which would
        hold the ``valid_until`` value.
    :param dict extra: Extra variables to add to the request.
    :param str extra_param: Name of the GET param name which would hold the
        ``extra_keys`` value.
    :param signature_cls:
    :return str:

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
        extra=extra
    )

    request_helper = RequestHelper(
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra_param=extra_param,
        signature_cls=signature_cls
    )

    signed_url = request_helper.signature_to_url(
        signature=signature,
        endpoint_url=url,
        suffix=suffix,
    )

    return signed_url


def signature_to_dict(auth_user,
                      secret_key,
                      valid_until=None,
                      lifetime=SIGNATURE_LIFETIME,
                      signature_param=DEFAULT_SIGNATURE_PARAM,
                      auth_user_param=DEFAULT_AUTH_USER_PARAM,
                      valid_until_param=DEFAULT_VALID_UNTIL_PARAM,
                      extra=None,
                      extra_param=DEFAULT_EXTRA_PARAM,
                      signature_cls=Signature):
    """Return a dictionary containing the signature data params.

    :param str auth_user: Username of the user making the request.
    :param str secret_key: The shared secret key.
    :param float|str valid_until: Unix timestamp. If not given, generated
        automatically (now + lifetime).
    :param int lifetime: Signature lifetime in seconds.
    :param str signature_param: Name of the (for example POST) param name
        which would hold the generated ``signature`` value.
    :param str auth_user_param: Name of the (for example POST) param name
        which would hold the ``auth_user`` value.
    :param str valid_until_param: Name of the (for example POST) param name
        which would hold the ``valid_until`` value.
    :param dict extra: Additional arguments for the signature.
    :param str extra_param: Name of the (for example POST) param name which
        would hold the ``extra`` keys value.
    :param signature_cls:
    :return str:

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
        extra=extra
    )

    request_helper = RequestHelper(
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra_param=extra_param,
        signature_cls=signature_cls
    )

    signature_dict = request_helper.signature_to_dict(
        signature=signature
    )

    return signature_dict


def validate_signed_request_data(data,
                                 secret_key,
                                 signature_param=DEFAULT_SIGNATURE_PARAM,
                                 auth_user_param=DEFAULT_AUTH_USER_PARAM,
                                 valid_until_param=DEFAULT_VALID_UNTIL_PARAM,
                                 extra_param=DEFAULT_EXTRA_PARAM,
                                 signature_cls=Signature):
    """Validate the signed request data.

    :param dict data: Dictionary holding the (HTTP) request (for example GET
        or POST) data.
    :param str secret_key: The shared secret key.
    :param str signature_param: Name of the (for example GET or POST) param
        name which holds the ``signature`` value.
    :param str auth_user_param: Name of the (for example GET or POST) param
        name which holds the ``auth_user`` value.
    :param str valid_until_param: Name of the (foe example GET or POST)
        param name which holds the ``valid_until`` value.
    :param str extra_param: Name of the (foe example GET or POST) param
        name which holds the ``extra`` keys value.
    :param signature_cls:
    :return ska.SignatureValidationResult: A ``ska.SignatureValidationResult``
        object with the following properties:
            - `result` (bool): True if data is valid. False otherwise.
            - `reason` (list): List of strings, indicating validation errors.
              Empty list in case if `result` is True.
    """
    request_helper = RequestHelper(
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra_param=extra_param,
        signature_cls=signature_cls
    )

    validation_result = request_helper.validate_request_data(
        data=data,
        secret_key=secret_key
    )

    return validation_result


def extract_signed_request_data(data,
                                secret_key=None,
                                signature_param=DEFAULT_SIGNATURE_PARAM,
                                auth_user_param=DEFAULT_AUTH_USER_PARAM,
                                valid_until_param=DEFAULT_VALID_UNTIL_PARAM,
                                extra_param=DEFAULT_EXTRA_PARAM,
                                validate=False,
                                fail_silently=False,
                                signature_cls=Signature):
    """Validate the signed request data.

    :param dict data: Dictionary holding the (HTTP) request (for example
        GET or POST) data.
    :param str secret_key: The shared secret key.
    :param str signature_param: Name of the (for example GET or POST) param
        name which holds the ``signature`` value.
    :param str auth_user_param: Name of the (for example GET or POST) param
        name which holds the ``auth_user`` value.
    :param str valid_until_param: Name of the (foe example GET or POST) param
        name which holds the ``valid_until`` value.
    :param str extra_param: Name of the (foe example GET or POST) param name
        which holds the ``extra`` value.
    :param bool validate: If set to True, request data is validated before
        returning the result.
    :param bool fail_silently: If set to True, exceptions are omitted.
    :param signature_cls:
    :return dict: Dictionary with signed request data.
    """
    request_helper = RequestHelper(
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra_param=extra_param,
        signature_cls=signature_cls
    )

    return request_helper.extract_signed_data(
        data,
        secret_key=secret_key,
        validate=validate,
        fail_silently=fail_silently
    )
