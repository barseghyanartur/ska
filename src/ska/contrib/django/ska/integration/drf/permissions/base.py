from __future__ import absolute_import
import logging

from ....... import validate_signed_request_data
from .......defaults import (
    DEFAULT_SIGNATURE_PARAM,
    DEFAULT_AUTH_USER_PARAM,
    DEFAULT_VALID_UNTIL_PARAM,
    DEFAULT_EXTRA_PARAM,
)
from .......exceptions import ImproperlyConfigured, InvalidData

from ....utils import get_provider_data

from rest_framework import permissions

__title__ = 'ska.contrib.django.ska.integration.drf.permissions.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'AbstractSignedRequestRequired',
    'BaseSignedRequestRequired',
    'BaseProviderSignedRequestRequired',
)

logger = logging.getLogger(__file__)


class AbstractSignedRequestRequired(permissions.BasePermission):
    """Signed request required permission."""

    def get_settings(self):
        """Get settings.

        :return:
        """
        raise NotImplementedError(
            "You should implement this method in your permission class"
        )

    def get_secret_key(self, request_data, request=None, view=None, obj=None):
        """Get secret key.

        :param request_data:
        :param request:
        :param view:
        :param obj:
        :return:
        """
        raise NotImplementedError(
            "You should implement this method in your permission class"
        )

    def validate_signed_request(self, request, view, obj=None):
        """Validate signed request.

        :param request:
        :param view:
        :param obj:
        :return:
        """
        request_data = request.GET.dict()

        secret_key = self.get_secret_key(
            request_data,
            request,
            view,
            obj
        )

        if not secret_key:
            return False

        try:
            # If authentication/data validation failed.
            validation_result = validate_signed_request_data(
                data=request_data,
                secret_key=secret_key,
                signature_param=DEFAULT_SIGNATURE_PARAM,
                auth_user_param=DEFAULT_AUTH_USER_PARAM,
                valid_until_param=DEFAULT_VALID_UNTIL_PARAM,
                extra_param=DEFAULT_EXTRA_PARAM
            )
            return validation_result.result
        except (ImproperlyConfigured, InvalidData) as err:
            logger.debug(str(err))
            return False

    def has_permission(self, request, view):
        return self.validate_signed_request(request, view)

    def has_object_permission(self, request, view, obj):
        return self.validate_signed_request(request, view, obj)


class BaseSignedRequestRequired(AbstractSignedRequestRequired):
    """Signed request required permission."""

    def get_secret_key(self, request_data, request=None, view=None, obj=None):
        """Get secret key.

        :param request_data:
        :param request:
        :param view:
        :param obj:
        :return:
        """
        settings = self.get_settings()
        return settings.get('SECRET_KEY', None)


class BaseProviderSignedRequestRequired(AbstractSignedRequestRequired):
    """Provider signed request required permission."""

    def get_secret_key(self, request_data, request=None, view=None, obj=None):
        """Get secret key.

        :param request_data:
        :param request:
        :param view:
        :param obj:
        :return:
        """
        provider_settings = self.get_settings()
        provider_data = get_provider_data(request_data, provider_settings)
        if provider_data:
            secret_key = provider_data['SECRET_KEY']
            return secret_key
