from __future__ import absolute_import

__title__ = 'ska.contrib.django.ska.http'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('HttpResponseUnauthorized',)

from django.http import HttpResponseForbidden

class HttpResponseUnauthorized(HttpResponseForbidden):
    """
    http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error
    """
    status_code = 401
