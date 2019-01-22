"""
- `UNAUTHORISED_REQUEST_ERROR_MESSAGE` (str): Plain text error message.
  Defaults to "Unauthorised request. {0}".
- `UNAUTHORISED_REQUEST_ERROR_TEMPLATE` (str): Path to 401 template that
  should be rendered in case of 401 responses. Defaults to empty string (not
  provided).
- `AUTH_USER` (str): Default ``auth_user`` for ``ska.sign_url`` function.
  Defaults to "ska-auth-user".
- `USER_GET_CALLBACK` (str): User get callback (when user is fetched in auth
  backend).
- `USER_VALIDATE_CALLBACK` (str): User validate callback (fired before user is
  created; created to allow custom logic to the user authentication before
  user object is even created).
- `USER_CREATE_CALLBACK` (str): User create callback (when user is created in
  auth backend).
- `USER_INFO_CALLBACK` (str): User info callback.
- `REDIRECT_AFTER_LOGIN` (str): Redirect after login.
- `DB_STORE_SIGNATURES` (bool): If set to True, signatures are stored in the
  database.
- `DB_PERFORM_SIGNATURE_CHECK` (bool): If set to True, an extra check is
  fired on whether the token has already been used or not.
- `PROVIDERS` (dict): A dictionary where key is the provider UID and the key
  is another dictionary holding the following provider specific keys:
  'SECRET_KEY', 'USER_GET_CALLBACK', 'USER_CREATE_CALLBACK',
  'USER_INFO_CALLBACK', 'REDIRECT_AFTER_LOGIN'. Note, that the 'SECRET_KEY'
  is a required key. The rest are optional, and if given, override
  respectively the values of ``ska.contrib.django.ska.settings``.
"""

from __future__ import absolute_import

from ska.gettext import _

__title__ = 'ska.contrib.django.ska.defaults'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'AUTH_USER',
    'DB_PERFORM_SIGNATURE_CHECK',
    'DB_STORE_SIGNATURES',
    'PROVIDERS',
    'REDIRECT_AFTER_LOGIN',
    'UNAUTHORISED_REQUEST_ERROR_MESSAGE',
    'UNAUTHORISED_REQUEST_ERROR_TEMPLATE',
    'USER_CREATE_CALLBACK',
    'USER_GET_CALLBACK',
    'USER_INFO_CALLBACK',
    'USER_VALIDATE_CALLBACK',
)

AUTH_USER = 'ska-auth-user'

UNAUTHORISED_REQUEST_ERROR_MESSAGE = _("Unauthorised request. {0}")

UNAUTHORISED_REQUEST_ERROR_TEMPLATE = ''

USER_VALIDATE_CALLBACK = None
USER_GET_CALLBACK = None
USER_CREATE_CALLBACK = None
USER_INFO_CALLBACK = None
REDIRECT_AFTER_LOGIN = ''

DB_STORE_SIGNATURES = False
DB_PERFORM_SIGNATURE_CHECK = False

PROVIDERS = {}
