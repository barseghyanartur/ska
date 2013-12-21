"""
Application defaults.

- `SIGNATURE_LIFETIME` (int): Signature lifetime in seconds. Default value is 600 (seconds).
- `DEFAULT_SIGNATURE_PARAM` (str): Default name of the GET param holding the generated signature value.
  Default value is `signature`.
- `DEFAULT_AUTH_USER_PARAM` (str): Default name of the GET param holding the ``auth_user`` value.
  Default value is `auth_user`.
- `DEFAULT_VALID_UNTIL_PARAM` (str): Default name of the GET param holding the ``valid_until`` value.
  Default value is `valid_until`.
- `DEFAULT_EXTRA_PARAM` (str): Default name of the GET param holding the ``extra`` value.
  Default value is `extra`.
- `DEFAULT_PROVIDER_PARAM` (str): Default name of the GET param holding the ``provider`` value.
  Default value is `provider`.
- `DEFAULT_URL_SUFFIX` (str): Suffix to add after the ``endpoint_url`` and before the appended signature
  params.
- `DEFAULT_RESERVED_PARAMS` (list): List of GET params reserved by default. Users should not be allowed
  to use them.
"""

__title__ = 'ska.defaults'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'TIMESTAMP_FORMAT', 'SIGNATURE_LIFETIME', 'DEFAULT_SIGNATURE_PARAM', 'DEFAULT_AUTH_USER_PARAM',
    'DEFAULT_VALID_UNTIL_PARAM', 'DEFAULT_EXTRA_PARAM', 'DEFAULT_PROVIDER_PARAM', 'DEFAULT_URL_SUFFIX',
    'DEFAULT_RESERVED_PARAMS', 'DEBUG'
    )

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

# Signature lifetime in seconds
SIGNATURE_LIFETIME = 600

# Default name of the GET param holding the generated signature value.
DEFAULT_SIGNATURE_PARAM = 'signature'

# Default name of the GET param holding the ``auth_user`` value.
DEFAULT_AUTH_USER_PARAM = 'auth_user'

# Default name of the GET param holding the ``valid_until`` value.
DEFAULT_VALID_UNTIL_PARAM = 'valid_until'

# Default name of the GET param holding the ``extra`` value.
DEFAULT_EXTRA_PARAM = 'extra'

# Default name of the GET param holding the ``provider`` value.
DEFAULT_PROVIDER_PARAM = 'provider'

# Suffix to add after the ``endpoint_url`` and before the appended signature params.
DEFAULT_URL_SUFFIX = '?'

# A list of GET params reserved by default. Users should not be allowed to use them.
DEFAULT_RESERVED_PARAMS = (
    DEFAULT_SIGNATURE_PARAM,
    DEFAULT_AUTH_USER_PARAM,
    DEFAULT_VALID_UNTIL_PARAM,
    DEFAULT_EXTRA_PARAM,
    DEFAULT_PROVIDER_PARAM
)

DEBUG = False
