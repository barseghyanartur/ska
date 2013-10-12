__title__ = 'ska.contrib.django.ska.settings'
__version__ = '0.8'
__build__ = 0x000008
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('UNAUTHORISED_REQUEST_ERROR_MESSAGE', 'AUTH_USER', 'SECRET_KEY')

from django.conf import settings

from ska.contrib.django.ska.conf import get_setting
from ska.contrib.django.ska.exceptions import ImproperlyConfigured

UNAUTHORISED_REQUEST_ERROR_MESSAGE = get_setting('UNAUTHORISED_REQUEST_ERROR_MESSAGE')

AUTH_USER = get_setting('AUTH_USER')

try:
    SECRET_KEY = settings.SKA_SECRET_KEY
except:
    raise ImproperlyConfigured("You should defined a variable ``SKA_SECRET_KEY`` in your `settings` module!")
