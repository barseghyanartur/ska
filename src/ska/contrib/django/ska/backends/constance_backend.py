from __future__ import absolute_import
import json
import logging

from constance import config

from django.conf import settings

from .base import BaseSkaAuthenticationBackend

logger = logging.getLogger(__file__)

__title__ = 'ska.contrib.django.ska.backends.constance_backend'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SkaAuthenticationConstanceBackend',)


class SkaAuthenticationConstanceBackend(BaseSkaAuthenticationBackend):
    """Authentication backend."""

    def get_settings(self):
        """Get settings.

        :return:
        """
        parse_from_json = getattr(
            settings,
            'SKA_CONSTANCE_SETTINGS_PARSE_FROM_JSON',
            False
        )
        if parse_from_json:
            try:
                _settings = json.loads(config.SKA_PROVIDERS)
                return _settings
            except ValueError as err:
                pass
        return config.SKA_PROVIDERS

    def get_secret_key(self):
        """Get secret key.

        :return:
        """
        return config.SKA_SECRET_KEY
