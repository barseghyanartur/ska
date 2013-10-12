from __future__ import absolute_import

__title__ = 'ska.contrib.django.ska.http'
__version__ = '0.8'
__build__ = 0x000008
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('HttpResponseUnauthorized',)

from django.http import HttpResponseForbidden

class HttpResponseUnauthorized(HttpResponseForbidden):
    """
    http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error
    """
    status_code = 401
