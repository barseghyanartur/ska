"""
Application defaults.

- `SIGNATURE_LIFETIME` (int): Signature lifetime in seconds. Default value is 600 (seconds).
- `DEFAULT_SIGNATURE_PARAM` (str): Default name of the GET param holding the generated signature value.
  Default value is `signature`.
- `DEFAULT_AUTH_USER_PARAM` (str): Default name of the GET param holding the ``auth_user`` value.
  Default value is `auth_user`.
- `DEFAULT_VALID_UNTIL_PARAM` (str): Default name of the GET param holding the ``valid_until`` value.
  Default value is `valid_until`.
- `DEFAULT_URL_SUFFIX` (str): Suffix to add after the ``endpoint_url`` and before the appended signature
  params.
"""

__title__ = 'ska.defaults'
__version__ = '0.7'
__build__ = 0x000007
__author__ = 'Artur Barseghyan'
__all__ = ('TIMESTAMP_FORMAT', 'SIGNATURE_LIFETIME', 'DEFAULT_SIGNATURE_PARAM', 'DEFAULT_AUTH_USER_PARAM', \
           'DEFAULT_VALID_UNTIL_PARAM', 'DEFAULT_URL_SUFFIX', 'DEBUG')

TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

# Signature lifetime in seconds
SIGNATURE_LIFETIME = 600

# Default name of the GET param holding the generated signature value.
DEFAULT_SIGNATURE_PARAM = 'signature'

# Default name of the GET param holding the ``auth_user`` value.
DEFAULT_AUTH_USER_PARAM = 'auth_user'

# Default name of the GET param holding the ``valid_until`` value.
DEFAULT_VALID_UNTIL_PARAM = 'valid_until'

# Suffix to add after the ``endpoint_url`` and before the appended signature params.
DEFAULT_URL_SUFFIX = '?'

DEBUG = False
