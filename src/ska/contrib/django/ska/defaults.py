"""
- `UNAUTHORISED_REQUEST_ERROR_MESSAGE` (str): Plain text error message. Defaults to "Unauthorised request. {0}".
- `UNAUTHORISED_REQUEST_ERROR_TEMPLATE` (str): Path to 401 template that should be rendered in case of 401
  responses. Defaults to empty string (not provided).
- `AUTH_USER` (str): Default ``auth_user`` for ``ska.sign_url`` function. Defaults to "ska-auth-user".
"""

__title__ = 'ska.contrib.django.ska.defaults'
__version__ = '0.9'
__build__ = 0x000009
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('AUTH_USER', 'UNAUTHORISED_REQUEST_ERROR_MESSAGE', 'UNAUTHORISED_REQUEST_ERROR_TEMPLATE')

ugettext = lambda s: s

AUTH_USER = 'ska-auth-user'

UNAUTHORISED_REQUEST_ERROR_MESSAGE = ugettext("Unauthorised request. {0}")

UNAUTHORISED_REQUEST_ERROR_TEMPLATE = ''
