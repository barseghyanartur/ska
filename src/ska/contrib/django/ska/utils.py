from datetime import datetime
from typing import Dict, Optional, Union

from django.conf import settings
from django.shortcuts import resolve_url
from django.utils.http import url_has_allowed_host_and_scheme

from ....defaults import DEFAULT_PROVIDER_PARAM
from .models import Signature
from .settings import PROVIDERS, REDIRECT_AFTER_LOGIN, SECRET_KEY

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = (
    "get_provider_data",
    "get_secret_key",
    "get_safe_redirect_target",
    "purge_signature_data",
)


def get_safe_redirect_target(request, target):
    """
    Return a safe redirect target:
      - If target is a safe relative URL or an allowed-host absolute URL -> return it.
      - Otherwise return a resolved fallback (REDIRECT_AFTER_LOGIN, settings.LOGIN_REDIRECT_URL, or '/').
    """
    allowed_hosts = {request.get_host()} | set(
        getattr(settings, "ALLOWED_HOSTS", [])
    )
    require_https = request.is_secure()

    if target and url_has_allowed_host_and_scheme(
        target, allowed_hosts=allowed_hosts, require_https=require_https
    ):
        return target

    fallback = REDIRECT_AFTER_LOGIN or getattr(
        settings, "LOGIN_REDIRECT_URL", "/"
    )
    return resolve_url(fallback)


def purge_signature_data() -> None:
    """Purge old signature data (valid_until < now)."""
    Signature._default_manager.filter(valid_until__lt=datetime.now()).delete()


def get_secret_key(
    data: Optional[Dict[str, Union[bytes, str, float, int]]],
    default: str = SECRET_KEY,
) -> str:
    """Obtain the secret key from request data given.

    This happens by looking up the secret key by `provider` param from the
    request data in the dictionary of ``PROVIDERS`` defined in settings
    module. If not found, fall back to the ``default`` value given, which is
    by default the globally set secret key.

    :param dict data:
    :param string default: Secret key value to be used as default. By default,
        the globally set secret key is used.
    """
    provider = data.get(DEFAULT_PROVIDER_PARAM, None)
    if provider:
        provider_data = PROVIDERS.get(provider, None)
        if provider_data:
            return provider_data.get("SECRET_KEY", default)

    return default


def get_provider_data(
    data: Dict[str, Union[bytes, str, float, int]],
    settings: Optional[Dict[str, Dict[str, str]]] = None,
) -> Optional[Dict[str, str]]:
    """Obtain the secret key from request data given.

    This happens by looking up the secret key by `provider` param from the
    request data in the dictionary of ``PROVIDERS`` defined in settings
    module. If not found, fall back to the ``default`` value given, which is
    by default the globally set secret key.

    :param dict data:
    :param dict settings: Settings dict.
    """
    if not settings or not isinstance(settings, dict):
        settings = PROVIDERS
    provider = data.get(DEFAULT_PROVIDER_PARAM)
    if provider:
        return settings.get(provider, None)
    return {}
