from django.http import HttpResponseForbidden

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("HttpResponseUnauthorized",)


class HttpResponseUnauthorized(HttpResponseForbidden):
    """HttpResponseUnauthorized.

    https://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error
    """

    status_code = 401
