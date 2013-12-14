__title__ = 'ska.contrib.django.ska.views'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('login',)

from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib import messages

from ska.contrib.django.ska.settings import REDIRECT_AFTER_LOGIN
from ska.contrib.django.ska.decorators import validate_signed_request

@validate_signed_request()
def login(request):
    """
    Authenticate with `ska` token into Django.

    :param django.http.HttpRequest request:
    :return django.http.HttpResponse:
    """
    user = authenticate(request=request)
    next_url = request.GET.get('next', REDIRECT_AFTER_LOGIN)

    if user is not None:
        auth_login(request, user)
        name = user.first_name or user.username
        messages.info(request, _("Login succeeded. Welcome, {0}.").format(name))
        return HttpResponseRedirect(next_url)
    else:
        return HttpResponseForbidden("Error authenticating with `ska`")
