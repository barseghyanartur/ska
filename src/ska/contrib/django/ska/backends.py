__title__ = 'ska.contrib.django.ska.backends'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SkaAuthenticationBackend',)

from django.contrib.auth.models import User, UNUSABLE_PASSWORD

from ska import validate_signed_request_data
from ska.helpers import get_callback_func
from ska.defaults import DEFAULT_SIGNATURE_PARAM, DEFAULT_AUTH_USER_PARAM, DEFAULT_VALID_UNTIL_PARAM
from ska.contrib.django.ska.settings import SECRET_KEY, USER_GET_CALLBACK, USER_CREATE_CALLBACK, USER_INFO_CALLBACK

class SkaAuthenticationBackend(object):
    """
    Authentication backend.
    """
    def authenticate(self, request):
        """
        :param django.http.HttpRequest request:
        :return django.contrib.auth.models.User: Instance or None on failure.
        """
        validation_result = validate_signed_request_data(
            data = request.REQUEST,
            secret_key = SECRET_KEY,
            signature_param = DEFAULT_SIGNATURE_PARAM,
            auth_user_param = DEFAULT_AUTH_USER_PARAM,
            valid_until_param = DEFAULT_VALID_UNTIL_PARAM
            )

        # If authentication failed.
        if not validation_result.result:
            return None

        # Get the username from request.
        auth_user = request.REQUEST.get(DEFAULT_AUTH_USER_PARAM)

        # Try to get user. If doesn't exist - create.
        try:
            user = User._default_manager.get(username=auth_user)

            # User get callback
            if USER_GET_CALLBACK is not None:
                callback_func = get_callback_func(USER_GET_CALLBACK)
                if callback_func:
                    callback_func(user)

        except User.DoesNotExist as e:
            user = User._default_manager.create_user(auth_user, UNUSABLE_PASSWORD)
            user.save()

            # User create callback
            if USER_CREATE_CALLBACK is not None:
                callback_func = get_callback_func(USER_CREATE_CALLBACK)
                if callback_func:
                    callback_func(user)

        # User info callback
        if USER_INFO_CALLBACK is not None:
            callback_func = get_callback_func(USER_INFO_CALLBACK)
            if callback_func:
                callback_func(user)

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
