from __future__ import absolute_import

from django.http import HttpResponseForbidden

__title__ = 'ska.contrib.django.ska.http'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('HttpResponseUnauthorized',)


class HttpResponseUnauthorized(HttpResponseForbidden):
    """HttpResponseUnauthorized.

    http://en.wikipedia.org/wiki/List_of_HTTP_status_codes#4xx_Client_Error
    """
    status_code = 401
