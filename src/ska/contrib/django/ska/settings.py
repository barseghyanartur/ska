from __future__ import absolute_import

"""
- `UNAUTHORISED_REQUEST_ERROR_MESSAGE` (str): Plain text error message. Defaults to "Unauthorised request. {0}".
- `UNAUTHORISED_REQUEST_ERROR_TEMPLATE` (str): Path to 401 template that should be rendered in case of 401
  responses. Defaults to empty string (not provided).
- `AUTH_USER` (str): Default ``auth_user`` for ``ska.sign_url`` function. Defaults to "ska-auth-user".
- `SECRET_KEY` (str): The shared secret key. Should be defined in `settings` module as ``SKA_SECRET_KEY``.
- `USER_GET_CALLBACK` (str): User get callback (when user is fetched in auth backend).
- `USER_CREATE_CALLBACK` (str): User create callback (when user is created in auth backend).
- `USER_INFO_CALLBACK` (str): User info callback.
- `REDIRECT_AFTER_LOGIN` (str): Redirect after login.
- `DB_STORE_SIGNATURES` (bool): If set to True, signatures are stored in the database.
- `DB_PERFORM_SIGNATURE_CHECK` (bool): If set to True, an extra check is fired on whether the token has
  already been used or not.
"""

__title__ = 'ska.contrib.django.ska.settings'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'UNAUTHORISED_REQUEST_ERROR_MESSAGE', 'UNAUTHORISED_REQUEST_ERROR_TEMPLATE', 'AUTH_USER', 'SECRET_KEY',
    'USER_GET_CALLBACK', 'USER_CREATE_CALLBACK', 'USER_INFO_CALLBACK', 'REDIRECT_AFTER_LOGIN',
    'DB_STORE_SIGNATURES', 'DB_PERFORM_SIGNATURE_CHECK'
)

from django.conf import settings

from ska.exceptions import ImproperlyConfigured
from ska.contrib.django.ska.conf import get_setting

UNAUTHORISED_REQUEST_ERROR_MESSAGE = get_setting('UNAUTHORISED_REQUEST_ERROR_MESSAGE')
UNAUTHORISED_REQUEST_ERROR_TEMPLATE = get_setting('UNAUTHORISED_REQUEST_ERROR_TEMPLATE')
AUTH_USER = get_setting('AUTH_USER')

try:
    SECRET_KEY = settings.SKA_SECRET_KEY
except:
    raise ImproperlyConfigured("You should defined a variable ``SKA_SECRET_KEY`` in your `settings` module!")

USER_GET_CALLBACK = get_setting('USER_GET_CALLBACK')
USER_CREATE_CALLBACK = get_setting('USER_CREATE_CALLBACK')
USER_INFO_CALLBACK = get_setting('USER_INFO_CALLBACK')
REDIRECT_AFTER_LOGIN = get_setting('REDIRECT_AFTER_LOGIN')

DB_STORE_SIGNATURES = get_setting('DB_STORE_SIGNATURES')
DB_PERFORM_SIGNATURE_CHECK = get_setting('DB_PERFORM_SIGNATURE_CHECK')
