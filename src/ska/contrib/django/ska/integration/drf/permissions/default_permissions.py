from ....settings import (
    SECRET_KEY,
    PROVIDERS,
)

from .base import (
    BaseProviderSignedRequestRequired,
    BaseSignedRequestRequired,
)

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = (
    "SignedRequestRequired",
    "ProviderSignedRequestRequired",
)


class SignedRequestRequired(BaseSignedRequestRequired):
    """Signed request required permission."""

    def get_settings(self, request_data, request=None, view=None, obj=None):
        return {
            "SECRET_KEY": SECRET_KEY,
        }


class ProviderSignedRequestRequired(BaseProviderSignedRequestRequired):
    """Provider signed request required permission."""

    def get_settings(self, request_data, request=None, view=None, obj=None):
        return PROVIDERS
