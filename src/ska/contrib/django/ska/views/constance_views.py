from constance import config

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils.translation import gettext, gettext_lazy as _

from ..settings import REDIRECT_AFTER_LOGIN
from ..utils import get_provider_data

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("constance_login",)


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
        return HttpResponseRedirect(next_url)
    else:
        return HttpResponseForbidden(_("Authentication error!"))
