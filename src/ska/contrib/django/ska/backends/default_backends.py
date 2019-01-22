from __future__ import absolute_import

import logging

from .base import BaseSkaAuthenticationBackend

logger = logging.getLogger(__file__)

__title__ = 'ska.contrib.django.ska.backends.default_backend'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SkaAuthenticationBackend',)


class SkaAuthenticationBackend(BaseSkaAuthenticationBackend):
    """Authentication backend."""

    def get_settings(self):
        """Get settings.

        :return:
        """
        return {}

    def get_secret_key(self):
        """Get secret key.

        :return:
        """
