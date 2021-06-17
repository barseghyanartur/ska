from typing import Any, Dict, Optional, Union
from django.http import HttpRequest
from rest_framework.request import Request

from .base import BaseSkaAuthenticationBackend

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("SkaAuthenticationBackend",)


class SkaAuthenticationBackend(BaseSkaAuthenticationBackend):
    """Authentication backend."""

    def get_settings(
        self,
        request_data: Optional[
            Dict[str, Union[bytes, str, float, int]]
        ] = None,
        request: Optional[Union[Request, HttpRequest]] = None,
        **kwargs,
    ) -> Dict[Any, Any]:
        """Get settings.

        :return:
        """
        return {}

    def get_secret_key(
        self,
        request_data: Optional[
            Dict[str, Union[bytes, str, float, int]]
        ] = None,
        request: Optional[Union[Request, HttpRequest]] = None,
        **kwargs,
    ) -> None:
        """Get secret key.

        :return:
        """
