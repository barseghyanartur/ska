__title__ = 'ska.contrib.django.ska.backends'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SkaAuthenticationBackend',)

import logging

from ska import Signature, extract_signed_request_data #validate_signed_request_data, 
from ska.helpers import get_callback_func
from ska.defaults import (
    DEFAULT_SIGNATURE_PARAM, DEFAULT_AUTH_USER_PARAM, DEFAULT_VALID_UNTIL_PARAM, DEFAULT_EXTRA_PARAM
    )
from ska.exceptions import ImproperlyConfigured, InvalidData
from ska.contrib.django.ska.utils import get_provider_data

from django.contrib.auth.models import User, UNUSABLE_PASSWORD
from django.db import IntegrityError

from ska.contrib.django.ska.settings import (
    SECRET_KEY, USER_GET_CALLBACK, USER_CREATE_CALLBACK, USER_INFO_CALLBACK,
    DB_STORE_SIGNATURES, DB_PERFORM_SIGNATURE_CHECK
    )
from ska.contrib.django.ska.models import Signature as SignatureModel

logger = logging.getLogger(__file__)

class SkaAuthenticationBackend(object):
    """
    Authentication backend.
    """
    def authenticate(self, request):
        """
        :param django.http.HttpRequest request:
        :return django.contrib.auth.models.User: Instance or None on failure.
        """
        #secret_key = get_secret_key(request.REQUEST, default=SECRET_KEY)
        provider_data = get_provider_data(request.REQUEST)
        if provider_data:
            secret_key = provider_data['SECRET_KEY']
        else:
            secret_key = SECRET_KEY

        logger.debug('secret_key: {0}'.format(secret_key))

        #validation_result = validate_signed_request_data(
        #    data = request.REQUEST,
        #    secret_key = SECRET_KEY,
        #    signature_param = DEFAULT_SIGNATURE_PARAM,
        #    auth_user_param = DEFAULT_AUTH_USER_PARAM,
        #    valid_until_param = DEFAULT_VALID_UNTIL_PARAM
        #    )

        # If authentication failed.
        #if not validation_result.result:
        #    return None

        try:
            # If authentication/data validation failed.
            signed_request_data = extract_signed_request_data(
                data = request.REQUEST,
                secret_key = secret_key,
                signature_param = DEFAULT_SIGNATURE_PARAM,
                auth_user_param = DEFAULT_AUTH_USER_PARAM,
                valid_until_param = DEFAULT_VALID_UNTIL_PARAM,
                extra_param = DEFAULT_EXTRA_PARAM,
                validate = True,
                fail_silently = False
                )
        except (ImproperlyConfigured, InvalidData) as e:
            logger.debug(str(e))
            return None

        # Get the username from request.
        auth_user = request.REQUEST.get(DEFAULT_AUTH_USER_PARAM)
        signature = request.REQUEST.get(DEFAULT_SIGNATURE_PARAM)
        valid_until = request.REQUEST.get(DEFAULT_VALID_UNTIL_PARAM)

        # All other specific data is taken from signed request data
        email = signed_request_data.get('email', '')
        first_name = signed_request_data.get('first_name', '')
        last_name = signed_request_data.get('last_name', '')

        # Storing the signatures to database if set to be so.
        if DB_STORE_SIGNATURES:
            token = SignatureModel(
                auth_user = auth_user,
                signature = signature,
                valid_until = Signature.unix_timestamp_to_date(valid_until)
            )
            try:
                token.save()
            except IntegrityError as e:
                if DB_PERFORM_SIGNATURE_CHECK:
                    # Token has already been used. Do not authenticate.
                    return None

        # Try to get user. If doesn't exist - create.
        try:
            user = User._default_manager.get(username=auth_user)

            # User get callback
            user_get_callback = provider_data.get('USER_GET_CALLBACK', USER_GET_CALLBACK)
            if user_get_callback is not None:
                callback_func = get_callback_func(user_get_callback)
                if callback_func:
                    try:
                        callback_func(user, request=request, signed_request_data=signed_request_data)
                    except Exception as e:
                        logger.debug(str(e))

        except User.DoesNotExist as e:
            user = User._default_manager.create_user(
                username = auth_user,
                email = email,
                password = UNUSABLE_PASSWORD,
                first_name = first_name,
                last_name = last_name
                )
            user.save()

            # User create callback
            user_create_callback = provider_data.get('USER_CREATE_CALLBACK', USER_CREATE_CALLBACK)
            if user_create_callback is not None:
                callback_func = get_callback_func(user_create_callback)
                if callback_func:
                    try:
                        callback_func(user, request=request, signed_request_data=signed_request_data)
                    except Exception as e:
                        logger.debug(str(e))

        # User info callback
        user_info_callback = provider_data.get('USER_INFO_CALLBACK', USER_INFO_CALLBACK)
        if user_info_callback is not None:
            callback_func = get_callback_func(user_info_callback)
            if callback_func:
                try:
                    callback_func(user, request=request, signed_request_data=signed_request_data)
                except Exception as e:
                    logger.debug(str(e))

        return user

    def get_user(self, user_id):
        """
        Get user in the ``django.contrib.auth.models.User`` if exists.

        :param int user_id:
        :return django.contrib.auth.models.User:
        """
        try:
            return User._default_manager.get(pk=user_id)
        except User.DoesNotExist as e:
            return None
