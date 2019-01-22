from __future__ import absolute_import
import logging

from constance import config

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
        return config.SKA_PROVIDERS

    def get_secret_key(self):
        """Get secret key.

        :return:
        """
        return config.SKA_SECRET_KEY
