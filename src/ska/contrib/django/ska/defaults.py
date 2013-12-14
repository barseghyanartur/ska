"""
- `UNAUTHORISED_REQUEST_ERROR_MESSAGE` (str): Plain text error message. Defaults to "Unauthorised request. {0}".
- `UNAUTHORISED_REQUEST_ERROR_TEMPLATE` (str): Path to 401 template that should be rendered in case of 401
  responses. Defaults to empty string (not provided).
- `AUTH_USER` (str): Default ``auth_user`` for ``ska.sign_url`` function. Defaults to "ska-auth-user".
- `USER_GET_CALLBACK` (str): User get callback (when user is fetched in auth backend).
- `USER_CREATE_CALLBACK` (str): User create callback (when user is created in auth backend).
- `USER_INFO_CALLBACK` (str): User info callback.
- `REDIRECT_AFTER_LOGIN` (str): Redirect after login.
"""

__title__ = 'ska.contrib.django.ska.defaults'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'AUTH_USER', 'UNAUTHORISED_REQUEST_ERROR_MESSAGE', 'UNAUTHORISED_REQUEST_ERROR_TEMPLATE',
    'USER_GET_CALLBACK', 'USER_CREATE_CALLBACK', 'USER_INFO_CALLBACK', 'REDIRECT_AFTER_LOGIN'
)

ugettext = lambda s: s

AUTH_USER = 'ska-auth-user'

UNAUTHORISED_REQUEST_ERROR_MESSAGE = ugettext("Unauthorised request. {0}")

UNAUTHORISED_REQUEST_ERROR_TEMPLATE = ''

USER_GET_CALLBACK = None
USER_CREATE_CALLBACK = None
USER_INFO_CALLBACK = None
REDIRECT_AFTER_LOGIN = ''
