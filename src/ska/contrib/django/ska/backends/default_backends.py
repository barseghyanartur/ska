from .base import BaseSkaAuthenticationBackend

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("SkaAuthenticationBackend",)


class SkaAuthenticationBackend(BaseSkaAuthenticationBackend):
    """Authentication backend."""

    def get_settings(self, request_data=None, request=None, **kwargs):
        """Get settings.

        :return:
        """
        return {}

    def get_secret_key(self, request_data=None, request=None, **kwargs):
        """Get secret key.

        :return:
        """
