from typing import Dict, Optional, Union, Type, Callable
from urllib.parse import urlencode

from .base import AbstractSignature, SignatureValidationResult
from .defaults import (
    DEFAULT_URL_SUFFIX,
    DEFAULT_EXTRA_PARAM,
    DEFAULT_SIGNATURE_PARAM,
    DEFAULT_AUTH_USER_PARAM,
    DEFAULT_VALID_UNTIL_PARAM,
)
from .exceptions import InvalidData, ImproperlyConfigured
from .helpers import dict_keys, extract_signed_data as extract_signed_data
from .signatures import Signature

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("RequestHelper",)

# ***************************************************************************
# ***************************************************************************
# **************************** Request helper *******************************
# ***************************************************************************
# ***************************************************************************


class RequestHelper(object):
    """Request helper for easy put/extract of signature params from URLs."""

    def __init__(
        self,
        signature_param: str = DEFAULT_SIGNATURE_PARAM,
        auth_user_param: str = DEFAULT_AUTH_USER_PARAM,
        valid_until_param: str = DEFAULT_VALID_UNTIL_PARAM,
        extra_param: str = DEFAULT_EXTRA_PARAM,
        signature_cls: Type[AbstractSignature] = Signature,
    ) -> None:
        """Constructor.

        :param signature_param:
        :param auth_user_param:
        :param valid_until_param:
        :param extra_param:
        :param signature_cls:
        """
        self.signature_param = signature_param
        self.auth_user_param = auth_user_param
        self.valid_until_param = valid_until_param
        self.extra_param = extra_param
        self.signature_cls = signature_cls

    def signature_to_url(
        self,
        signature: AbstractSignature,
        endpoint_url: str = "",
        suffix: str = DEFAULT_URL_SUFFIX,
    ) -> str:
        """URL encodes the signature params.

        :param signature: Signature class.
        :param endpoint_url:
        :param suffix: Suffix to add after the ``endpoint_url`` and before
            the appended signature params.
        :return:

        :example:

        Required imports.

        >>> from ska import Signature, RequestHelper

        Generate signature.

        >>> signature = Signature.generate_signature(
        >>>     auth_user='user',
        >>>     secret_key='your-secret-key'
        >>> )

        Create a request helper.

        >>> request_helper = RequestHelper(
        >>>     signature_param='signature',
        >>>     auth_user_param='auth_user',
        >>>     valid_until_param='valid_until'
        >>> )

        Appending signature params to the endpoint URL.

        >>> url = request_helper.signature_to_url(
        >>>     signature=signature,
        >>>     endpoint_url='http://e.com/api/'
        >>> )
        http://e.com/api/?valid_until=1378045287.0&auth_user=user&signature=YlZpLFsjUKBalL4x5trhkeEgqE8%3D
        """
        params = {
            self.signature_param: signature.signature,
            self.auth_user_param: signature.auth_user,
            self.valid_until_param: signature.valid_until,
            self.extra_param: dict_keys(signature.extra, return_string=True),
        }

        # Make some check that params used do not overlap with names
        # reserved (`auth_user`, `signature`, etc).
        params.update(signature.extra)

        return f"{endpoint_url}{suffix}{urlencode(params)}"

    def signature_to_dict(
        self, signature: AbstractSignature
    ) -> Dict[str, Union[bytes, str, float, int]]:
        """Put signature into a dictionary.

         Dictionary can be used later on to send requests (for example, a POST
         request) to the server.

        :param signature: Signature class.
        :return:

        :example:

        Required imports.

        >>> from ska import Signature, RequestHelper

        Generate signature.

        >>> signature = Signature.generate_signature(
        >>>     auth_user='user',
        >>>     secret_key='your-secret-key'
        >>> )

        Create a request helper.

        >>> request_helper = RequestHelper(
        >>>     signature_param='signature',
        >>>     auth_user_param='auth_user',
        >>>     valid_until_param='valid_until'
        >>> )

        Appending signature params to the endpoint URL.

        >>> signed_dict = request_helper.signature_to_dict(
        >>>     signature=signature
        >>> )
        {
            'signature': 'YlZpLFsjUKBalL4x5trhkeEgqE8=',
            'auth_user': 'user',
            'valid_until': '1378045287.0'
        }
        """
        data = {
            self.signature_param: signature.signature,
            self.auth_user_param: signature.auth_user,
            self.valid_until_param: signature.valid_until,
            self.extra_param: dict_keys(signature.extra, return_string=True),
        }

        data.update(signature.extra)

        return data

    def validate_request_data(
        self,
        data: Dict[str, Union[bytes, str, float, int]],
        secret_key: str,
        value_dumper: Optional[Callable] = None,
        quoter: Optional[Callable] = None,
    ) -> SignatureValidationResult:
        """Validate the request data.

        :param data:
        :param secret_key:
        :param value_dumper:
        :param quoter:
        :return:

        :example:
        If your imaginary `HttpRequest` object has `GET` property (dict),
        then you would validate the request data as follows.

        Create a `RequestHelper` object with param names expected.

        Required imports.

        >>> from ska import RequestHelper

        Create a request helper.

        >>> request_helper = RequestHelper(
        >>>     signature_param='signature',
        >>>     auth_user_param='auth_user',
        >>>     valid_until_param='valid_until'
        >>> )

        Validate the request data.

        >>> validation_result = request_helper.validate_request_data(
        >>>     data=request.GET,
        >>>     secret_key='your-secret-key'
        >>> )
        """
        signature = data.get(self.signature_param, "")
        auth_user = data.get(self.auth_user_param, "")
        valid_until = data.get(self.valid_until_param, "")

        extra = extract_signed_data(
            data=data, extra=data.get(self.extra_param, "").split(",")
        )

        validation_result = self.signature_cls.validate_signature(
            signature=signature,
            auth_user=auth_user,
            secret_key=secret_key,
            valid_until=valid_until,
            return_object=True,
            extra=extra,
            value_dumper=value_dumper,
            quoter=quoter,
        )

        return validation_result

    def extract_signed_data(
        self,
        data: Dict[str, Union[bytes, str, float, int]],
        secret_key: Optional[str] = None,
        validate: bool = False,
        fail_silently: bool = False,
        value_dumper: Optional[Callable] = None,
        quoter: Optional[Callable] = None,
    ) -> Dict[str, str]:
        """Extract signed data from the request.

        :param data:
        :param secret_key:
        :param validate:
        :param fail_silently:
        :param value_dumper:
        :param quoter:
        :return:
        """
        if validate:
            if not secret_key:
                if fail_silently:
                    return {}
                raise ImproperlyConfigured(
                    "You should provide `secret_key` "
                    "if `validate` is set to True."
                )
            validation_result = self.validate_request_data(
                data,
                secret_key,
                value_dumper=value_dumper,
                quoter=quoter,
            )
            if not validation_result.result:
                if fail_silently:
                    return {}
                raise InvalidData(validation_result.message)

        return extract_signed_data(
            data=data, extra=data.get(self.extra_param, "").split(",")
        )
