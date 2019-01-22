from constance import config

from .base import (
    BaseProviderSignedRequestRequired,
    BaseSignedRequestRequired,
)

__title__ = 'ska.contrib.django.ska.integration.drf.permissions.' \
            'constance_permissions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'ConstanceSignedRequestRequired',
    'ConstanceProviderSignedRequestRequired',
)


class ConstanceSignedRequestRequired(BaseSignedRequestRequired):
    """Signed request required permission."""

    def get_settings(self):
        return {
            'SECRET_KEY': config.SKA_SECRET_KEY,
        }


class ConstanceProviderSignedRequestRequired(
    BaseProviderSignedRequestRequired
):
    """Provider signed request required permission."""

    def get_settings(self):
        return config.SKA_PROVIDERS
