from __future__ import absolute_import

"""
jskjfkfjkl
"""

__title__ = 'ska.contrib.django.ska.decorators'
__version__ = '0.8'
__build__ = 0x000008
__author__ = 'Artur Barseghyan'
__all__ = ('validate_signed_request', 'sign_url')

from six import PY2, text_type

from ska import validate_signed_request_data, sign_url as ska_sign_url
from ska.defaults import SIGNATURE_LIFETIME, DEFAULT_URL_SUFFIX, DEFAULT_SIGNATURE_PARAM, DEFAULT_AUTH_USER_PARAM
from ska.defaults import DEFAULT_VALID_UNTIL_PARAM

from ska.contrib.django.ska.settings import SECRET_KEY, AUTH_USER, UNAUTHORISED_REQUEST_ERROR_MESSAGE
from ska.contrib.django.ska.settings import UNAUTHORISED_REQUEST_ERROR_TEMPLATE
from ska.contrib.django.ska.http import HttpResponseUnauthorized

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render

class ValidateSignedRequest(object):
    """
    Function decorator. Validate request signature. Detects whether request is GET or POST and applied
    appropriate validation mechanism. Assumes ``SKA_SECRET_KEY`` to be in ``settings`` module.

    :attribute str secret_key:
    :attribute str signature_param:
    """
    def __init__(self, secret_key=SECRET_KEY, signature_param=DEFAULT_SIGNATURE_PARAM, \
                 auth_user_param=DEFAULT_AUTH_USER_PARAM, valid_until_param=DEFAULT_VALID_UNTIL_PARAM):
        self.secret_key = secret_key
        self.signature_param = signature_param
        self.auth_user_param = auth_user_param
        self.valid_until_param = valid_until_param

    def __call__(self, func):
        def inner(request, *args, **kwargs):
            # Validating the request.
            validation_result = validate_signed_request_data(
                data = request.REQUEST,
                secret_key = self.secret_key,
                signature_param = self.signature_param,
                auth_user_param = self.auth_user_param,
                valid_until_param = self.valid_until_param
                )
            if validation_result.result is True:
                # If validated, just return the func as is.
                return func(request, *args, **kwargs)
            else:
                # Otherwise...
                if UNAUTHORISED_REQUEST_ERROR_TEMPLATE:
                    # If template to display the error message is set in ska (django-ska) settings,
                    # use it to render the message and return ``HttpResponseUnauthorized`` response
                    # describing the error.
                    response_content = render(
                        request,
                        UNAUTHORISED_REQUEST_ERROR_TEMPLATE,
                        {'reason': '; '.join(validation_result.reason)}
                        )
                    return HttpResponseUnauthorized(response_content)
                else:
                    # Otherwise, return plain text message with describing the error.
                    return HttpResponseUnauthorized(
                        _(UNAUTHORISED_REQUEST_ERROR_MESSAGE).format('; '.join(validation_result.reason))
                        )
        return inner

validate_signed_request = ValidateSignedRequest


class SignAbsoluteURL(object):
    """
    Method decorator (to be used in models). Signs the URL.
    """
    def __init__(self, auth_user=AUTH_USER, secret_key=SECRET_KEY, valid_until=None, lifetime=SIGNATURE_LIFETIME, \
                 suffix=DEFAULT_URL_SUFFIX, signature_param=DEFAULT_SIGNATURE_PARAM, \
                 auth_user_param=DEFAULT_AUTH_USER_PARAM, valid_until_param=DEFAULT_VALID_UNTIL_PARAM):
        self.auth_user = auth_user
        self.secret_key = secret_key
        self.valid_until = valid_until
        self.lifetime = lifetime
        self.suffix = suffix
        self.signature_param = signature_param
        self.auth_user_param = auth_user_param
        self.valid_until_param = valid_until_param

    def __call__(self, func):
        def inner(this, *args, **kwargs):
            if PY2:
                url = text_type(func(this, *args, **kwargs))
            else:
                url = func(this, *args, **kwargs)

            return ska_sign_url(
                auth_user = self.auth_user,
                secret_key = self.secret_key,
                valid_until = self.valid_until,
                lifetime = self.lifetime,
                url = url,
                suffix = self.suffix,
                signature_param = self.signature_param,
                auth_user_param = self.auth_user_param,
                valid_until_param = self.valid_until_param
                )
        return inner

sign_url = SignAbsoluteURL
