from typing import Dict, Optional, Union

from django.db.models import Model
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet

from ....settings import PROVIDERS, SECRET_KEY
from .base import BaseProviderSignedRequestRequired, BaseSignedRequestRequired

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = (
    "ProviderSignedRequestRequired",
    "SignedRequestRequired",
)


class SignedRequestRequired(BaseSignedRequestRequired):
    """Signed request required permission."""

    def get_settings(
        self,
        request_data: Dict[str, Union[bytes, str, float, int]],
        request: Optional[Request] = None,
        view: Optional[GenericViewSet] = None,
        obj: Optional[Model] = None,
    ) -> Dict[str, str]:
        return {
            "SECRET_KEY": SECRET_KEY,
        }


class ProviderSignedRequestRequired(BaseProviderSignedRequestRequired):
    """Provider signed request required permission."""

    def get_settings(
        self,
        request_data: Dict[str, Union[bytes, str, float, int]],
        request: Optional[Request] = None,
        view: Optional[GenericViewSet] = None,
        obj: Optional[Model] = None,
    ) -> Dict[str, Dict[str, str]]:
        return PROVIDERS
