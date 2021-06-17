from typing import Dict, Optional, Union
import logging

from django.db.models import Model
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from ....... import validate_signed_request_data
from .......defaults import (
    DEFAULT_SIGNATURE_PARAM,
    DEFAULT_AUTH_USER_PARAM,
    DEFAULT_VALID_UNTIL_PARAM,
    DEFAULT_EXTRA_PARAM,
)
from .......exceptions import ImproperlyConfigured, InvalidData

from ....utils import get_provider_data


__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = (
    "AbstractSignedRequestRequired",
    "BaseSignedRequestRequired",
    "BaseProviderSignedRequestRequired",
)

LOGGER = logging.getLogger(__file__)


class AbstractSignedRequestRequired(permissions.BasePermission):
    """Signed request required permission."""

    def get_settings(
        self,
        request_data: Dict[str, Union[bytes, str, float, int]],
        request: Optional[Request] = None,
        view: Optional[GenericViewSet] = None,
        obj: Optional[Model] = None,
    ) -> Dict[str, str]:
        """Get settings.

        :return:
        """
        raise NotImplementedError(
            "You should implement this method in your permission class"
        )

    def get_secret_key(
        self,
        request_data: Dict[str, Union[bytes, str, float, int]],
        request: Optional[Request] = None,
        view: Optional[GenericViewSet] = None,
        obj: Optional[Model] = None,
    ):
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

    def get_request_data(
        self,
        request: Request,
        view: GenericViewSet,
        obj: Optional[Model] = None,
    ) -> Dict[str, Union[bytes, str, float, int]]:
        return request.GET.dict()

    def validate_signed_request(
        self,
        request: Request,
        view: GenericViewSet,
        obj: Optional[Model] = None,
    ) -> bool:
        """Validate signed request.

        :param request:
        :param view:
        :param obj:
        :return:
        """
        request_data = self.get_request_data(request, view, obj)

        secret_key = self.get_secret_key(request_data, request, view, obj)

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
                extra_param=DEFAULT_EXTRA_PARAM,
            )
            return validation_result.result
        except (ImproperlyConfigured, InvalidData) as err:
            LOGGER.debug(str(err))
            return False

    def has_permission(self, request: Request, view: GenericViewSet) -> bool:
        return self.validate_signed_request(request, view)

    def has_object_permission(
        self, request: Request, view: GenericViewSet, obj: Model
    ) -> bool:
        return self.validate_signed_request(request, view, obj)


class BaseSignedRequestRequired(AbstractSignedRequestRequired):
    """Signed request required permission."""

    def get_secret_key(
        self,
        request_data: Dict[str, str],
        request: Optional[Request] = None,
        view: Optional[GenericViewSet] = None,
        obj: Optional[Model] = None,
    ) -> str:
        """Get secret key.

        :param request_data:
        :param request:
        :param view:
        :param obj:
        :return:
        """
        settings = self.get_settings(
            request_data, request=None, view=None, obj=None
        )
        return settings.get("SECRET_KEY", None)


class BaseProviderSignedRequestRequired(AbstractSignedRequestRequired):
    """Provider signed request required permission."""

    def get_secret_key(
        self,
        request_data: Dict[str, str],
        request: Optional[Request] = None,
        view: Optional[GenericViewSet] = None,
        obj: Optional[Model] = None,
    ) -> Optional[str]:
        """Get secret key.

        :param request_data:
        :param request:
        :param view:
        :param obj:
        :return:
        """
        provider_settings = self.get_settings(
            request_data, request=None, view=None, obj=None
        )
        provider_data = get_provider_data(request_data, provider_settings)
        if provider_data:
            secret_key = provider_data["SECRET_KEY"]
            return secret_key
