from constance import config
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from django.utils.http import url_has_allowed_host_and_scheme

from ..settings import REDIRECT_AFTER_LOGIN
from ..utils import get_provider_data

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("constance_login",)


def _get_safe_redirect_target(request, target):
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


def constance_login(request):
    """Login.

    Authenticate with `ska` token into Django.

    :param django.http.HttpRequest request:
    :return django.http.HttpResponse:
    """
    user = authenticate(request=request)
    next_url = request.GET.get("next", None)

    if not next_url:
        request_data = request.GET.dict()
        settings = config.SKA_PROVIDERS
        provider_data = get_provider_data(request_data, settings)
        if provider_data:
            next_url = provider_data.get(
                "REDIRECT_AFTER_LOGIN", REDIRECT_AFTER_LOGIN
            )

    if not next_url:
        next_url = "/"

    if user is not None:
        auth_login(request, user)
        name = user.first_name or user.username
        messages.info(request, gettext(f"Login succeeded. Welcome, {name}."))
        safe_target = _get_safe_redirect_target(request, next_url)
        return HttpResponseRedirect(safe_target)
    else:
        return HttpResponseForbidden(_("Authentication error!"))
