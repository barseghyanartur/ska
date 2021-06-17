import json
from typing import Dict, Optional, Union

from constance import config

from django.conf import settings
from django.http import HttpRequest
from rest_framework.request import Request

from .base import BaseSkaAuthenticationBackend

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("SkaAuthenticationConstanceBackend",)


class SkaAuthenticationConstanceBackend(BaseSkaAuthenticationBackend):
    """Authentication backend."""

    def get_settings(
        self,
        request_data: Optional[
            Dict[str, Union[bytes, str, float, int]]
        ] = None,
        request: Optional[Union[Request, HttpRequest]] = None,
        **kwargs,
    ) -> Dict[str, Dict[str, str]]:
        """Get settings.

        :return:
        """
        parse_from_json = getattr(
            settings, "SKA_CONSTANCE_SETTINGS_PARSE_FROM_JSON", False
        )
        if parse_from_json:
            try:
                _settings = json.loads(config.SKA_PROVIDERS)
                return _settings
            except ValueError as err:
                pass
        return config.SKA_PROVIDERS

    def get_secret_key(
        self,
        request_data: Optional[
            Dict[str, Union[bytes, str, float, int]]
        ] = None,
        request: Optional[Union[Request, HttpRequest]] = None,
        **kwargs,
    ) -> str:
        """Get secret key.

        :return:
        """
        return config.SKA_SECRET_KEY
