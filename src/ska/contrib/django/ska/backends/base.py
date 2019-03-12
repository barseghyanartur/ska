from __future__ import absolute_import
import logging

from django.core.exceptions import PermissionDenied
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import IntegrityError

from nine import versions

from ..... import Signature, extract_signed_request_data
from .....helpers import get_callback_func
from .....defaults import (
    DEFAULT_SIGNATURE_PARAM,
    DEFAULT_AUTH_USER_PARAM,
    DEFAULT_VALID_UNTIL_PARAM,
    DEFAULT_EXTRA_PARAM,
)
from .....exceptions import ImproperlyConfigured, InvalidData

from ..models import Signature as SignatureModel
from ..settings import (
    DB_PERFORM_SIGNATURE_CHECK,
    DB_STORE_SIGNATURES,
    SECRET_KEY,
    USER_CREATE_CALLBACK,
    USER_GET_CALLBACK,
    USER_INFO_CALLBACK,
    USER_VALIDATE_CALLBACK,
)
from ..utils import get_provider_data

logger = logging.getLogger(__file__)

__title__ = 'ska.contrib.django.ska.backends.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('BaseSkaAuthenticationBackend',)


class BaseSkaAuthenticationBackend(object):
    """Base authentication backend."""

    def get_settings(self):
        """Get settings.

        :return:
        """
        raise NotImplementedError(
            "You should implement this method in your authentication backend"
        )

    def get_secret_key(self):
        """Get secret key.

        :return:
        """
        raise NotImplementedError(
            "You should implement this method in your authentication backend"
        )

    def authenticate(self, request, **kwargs):
        """Authenticate.

        :param django.http.HttpRequest request:
        :return django.contrib.auth.models.User: Instance or None on failure.
        """
        if request is None:
            logger.debug("Request is None, skipping")
            return None

        if versions.DJANGO_GTE_1_7:
            request_data = request.GET.dict()
        else:
            request_data = request.REQUEST

        provider_settings = self.get_settings()

        provider_data = get_provider_data(request_data, provider_settings)

        if provider_data:
            secret_key = provider_data['SECRET_KEY']
        else:
            secret_key = self.get_secret_key()
            if not secret_key:
                secret_key = SECRET_KEY

        try:
            # If authentication/data validation failed.
            signed_request_data = extract_signed_request_data(
                data=request_data,
                secret_key=secret_key,
                signature_param=DEFAULT_SIGNATURE_PARAM,
                auth_user_param=DEFAULT_AUTH_USER_PARAM,
                valid_until_param=DEFAULT_VALID_UNTIL_PARAM,
                extra_param=DEFAULT_EXTRA_PARAM,
                validate=True,
                fail_silently=False
            )
        except (ImproperlyConfigured, InvalidData) as err:
            logger.debug(str(err))
            return None

        # Get the username from request.
        auth_user = request_data.get(DEFAULT_AUTH_USER_PARAM)
        signature = request_data.get(DEFAULT_SIGNATURE_PARAM)
        valid_until = request_data.get(DEFAULT_VALID_UNTIL_PARAM)

        # All other specific data is taken from signed request data
        email = signed_request_data.get('email', '')
        first_name = signed_request_data.get('first_name', '')
        last_name = signed_request_data.get('last_name', '')

        # Validate request callback. Created to allow adding custom logic to
        # the incoming authentication requests. The main purpose is to provide
        # a flexible way of raising exceptions if the incoming authentication
        # request shall be blocked (for instance, email or username is in
        # black-list or right the opposite - not in the white list). The only
        # aim of the `USER_VALIDATE_CALLBACK` is to raise a
        # ``django.core.PermissionDenied`` exception if request data is
        # invalid. In that case, the authentication flow will halt. All
        # other exceptions would simply be ignored (but logged) and if no
        # exception raised, the normal flow would be continued.
        user_validate_callback = provider_data.get(
            'USER_VALIDATE_CALLBACK',
            USER_VALIDATE_CALLBACK
        )
        if user_validate_callback is not None:
            callback_func = get_callback_func(user_validate_callback)
            if callback_func:
                try:
                    user_validate_callback_resp = callback_func(
                        request=request,
                        signed_request_data=signed_request_data
                    )
                except PermissionDenied as err:
                    logger.debug(str(err))
                    raise err
                except Exception as err:
                    logger.debug(str(err))

        # Storing the signatures to database if set to be so.
        if DB_STORE_SIGNATURES:
            token = SignatureModel(
                auth_user=auth_user,
                signature=signature,
                valid_until=Signature.unix_timestamp_to_date(valid_until)
            )
            try:
                token.save()
            except IntegrityError:
                if DB_PERFORM_SIGNATURE_CHECK:
                    # Token has already been used. Do not authenticate.
                    return None

        # Try to get user. If doesn't exist - create.
        try:
            user = User._default_manager.get(username=auth_user)

            # User get callback
            user_get_callback = provider_data.get(
                'USER_GET_CALLBACK',
                USER_GET_CALLBACK
            )
            if user_get_callback is not None:
                callback_func = get_callback_func(user_get_callback)
                if callback_func:
                    try:
                        user_get_callback_resp = callback_func(
                            user,
                            request=request,
                            signed_request_data=signed_request_data
                        )
                    except Exception as err:
                        logger.debug(str(err))

        except User.DoesNotExist:
            user = User._default_manager.create_user(
                username=auth_user,
                email=email,
                password=make_password(password=None),
                first_name=first_name,
                last_name=last_name
            )
            user.save()

            # User create callback
            user_create_callback = provider_data.get(
                'USER_CREATE_CALLBACK',
                USER_CREATE_CALLBACK
            )
            if user_create_callback is not None:
                callback_func = get_callback_func(user_create_callback)
                if callback_func:
                    try:
                        user_create_callback_resp = callback_func(
                            user,
                            request=request,
                            signed_request_data=signed_request_data
                        )
                    except Exception as err:
                        logger.debug(str(err))

        # User info callback
        user_info_callback = provider_data.get(
            'USER_INFO_CALLBACK',
            USER_INFO_CALLBACK
        )
        if user_info_callback is not None:
            callback_func = get_callback_func(user_info_callback)
            if callback_func:
                try:
                    callback_func(
                        user,
                        request=request,
                        signed_request_data=signed_request_data
                    )
                except Exception as err:
                    logger.debug(str(err))

        return user

    def get_user(self, user_id):
        """Get user in the ``django.contrib.auth.models.User`` if exists.

        :param int user_id:
        :return django.contrib.auth.models.User:
        """
        try:
            return User._default_manager.get(pk=user_id)
        except User.DoesNotExist:
            return None
