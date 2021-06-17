from typing import Dict, Optional, Union

from constance import config

from django.db.models import Model
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from .base import (
    BaseProviderSignedRequestRequired,
    BaseSignedRequestRequired,
)

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = (
    "ConstanceSignedRequestRequired",
    "ConstanceProviderSignedRequestRequired",
)


class ConstanceSignedRequestRequired(BaseSignedRequestRequired):
    """Signed request required permission."""

    def get_settings(
        self,
        request_data: Dict[str, Union[bytes, str, float, int]],
        request: Optional[Request] = None,
        view: Optional[GenericViewSet] = None,
        obj: Optional[Model] = None,
    ) -> Dict[str, str]:
        return {
            "SECRET_KEY": config.SKA_SECRET_KEY,
        }


class ConstanceProviderSignedRequestRequired(
    BaseProviderSignedRequestRequired
):
    """Provider signed request required permission."""

    def get_settings(
        self,
        request_data: Dict[str, Union[bytes, str, float, int]],
        request: Optional[Request] = None,
        view: Optional[GenericViewSet] = None,
        obj: Optional[Model] = None,
    ) -> Dict[str, Dict[str, str]]:
        return config.SKA_PROVIDERS
