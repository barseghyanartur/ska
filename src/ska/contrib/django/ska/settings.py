"""
- `UNAUTHORISED_REQUEST_ERROR_MESSAGE` (str): Plain text error message.
  Defaults to "Unauthorised request. {0}".
- `UNAUTHORISED_REQUEST_ERROR_TEMPLATE` (str): Path to 401 template that
  should be rendered in case of 401 responses. Defaults to empty string (not
  provided).
- `AUTH_USER` (str): Default ``auth_user`` for ``ska.sign_url`` function.
  Defaults to "ska-auth-user".
- `SECRET_KEY` (str): The shared secret key. Should be defined in `settings`
  module as ``SKA_SECRET_KEY``.
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
- `DB_PERFORM_SIGNATURE_CHECK` (bool): If set to True, an extra check is fired
  on whether the token has already been used or not.
- `PROVIDERS` (dict): A dictionary where key is the provider UID and the key
  is another dictionary holding the following provider specific keys:
  'SECRET_KEY', 'USER_GET_CALLBACK', 'USER_CREATE_CALLBACK',
  'USER_INFO_CALLBACK', 'REDIRECT_AFTER_LOGIN'. Note, that the 'SECRET_KEY'
  is a required key. The rest are optional, and if given, override
  respectively the values of ``ska.contrib.django.ska.settings``.
"""

from __future__ import absolute_import

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from ....exceptions import ImproperlyConfigured
from .conf import get_setting

__title__ = 'ska.contrib.django.ska.settings'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'AUTH_USER',
    'DB_PERFORM_SIGNATURE_CHECK',
    'DB_STORE_SIGNATURES',
    'PROVIDERS',
    'REDIRECT_AFTER_LOGIN',
    'SECRET_KEY',
    'UNAUTHORISED_REQUEST_ERROR_MESSAGE',
    'UNAUTHORISED_REQUEST_ERROR_TEMPLATE',
    'USER_CREATE_CALLBACK',
    'USER_GET_CALLBACK',
    'USER_INFO_CALLBACK',
    'USER_VALIDATE_CALLBACK',
)

UNAUTHORISED_REQUEST_ERROR_MESSAGE = get_setting(
    'UNAUTHORISED_REQUEST_ERROR_MESSAGE'
)
UNAUTHORISED_REQUEST_ERROR_TEMPLATE = get_setting(
    'UNAUTHORISED_REQUEST_ERROR_TEMPLATE'
)
AUTH_USER = get_setting('AUTH_USER')

try:
    SECRET_KEY = settings.SKA_SECRET_KEY
except Exception:
    raise ImproperlyConfigured(
        _("You should define a variable ``SKA_SECRET_KEY`` in your "
          "`settings` module!")
    )

USER_VALIDATE_CALLBACK = get_setting('USER_VALIDATE_CALLBACK')
USER_GET_CALLBACK = get_setting('USER_GET_CALLBACK')
USER_CREATE_CALLBACK = get_setting('USER_CREATE_CALLBACK')
USER_INFO_CALLBACK = get_setting('USER_INFO_CALLBACK')
REDIRECT_AFTER_LOGIN = get_setting('REDIRECT_AFTER_LOGIN')

DB_STORE_SIGNATURES = get_setting('DB_STORE_SIGNATURES')
DB_PERFORM_SIGNATURE_CHECK = get_setting('DB_PERFORM_SIGNATURE_CHECK')

PROVIDERS = get_setting('PROVIDERS')


def validate_providers():
    """Validate providers set in Django `settings` module of the project."""
    for uid, data in PROVIDERS.items():
        if 'SECRET_KEY' not in data:
            raise ImproperlyConfigured(
                _("You should defined a key ``SECRET_KEY`` for each provider "
                  "in your `settings module`!")
            )


validate_providers()
