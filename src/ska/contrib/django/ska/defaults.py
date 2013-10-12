__title__ = 'ska.contrib.django.ska.defaults'
__version__ = '0.8'
__build__ = 0x000008
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('AUTH_USER', 'UNAUTHORISED_REQUEST_ERROR_MESSAGE', 'UNAUTHORISED_REQUEST_ERROR_TEMPLATE')

ugettext = lambda s: s

AUTH_USER = 'ska-auth-user'

UNAUTHORISED_REQUEST_ERROR_MESSAGE = ugettext("Unauthorised request. {0}")

UNAUTHORISED_REQUEST_ERROR_TEMPLATE = ''
