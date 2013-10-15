__title__ = 'ska.contrib.django.ska.exceptions'
__version__ = '0.9'
__build__ = 0x000009
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('ImproperlyConfigured',)

class ImproperlyConfigured(Exception):
    """
    Exception raised when developer didn't configure the code properly.
    """
