__title__ = 'ska.contrib.django.ska.exceptions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('ImproperlyConfigured',)

class ImproperlyConfigured(Exception):
    """
    Exception raised when developer didn't configure the code properly.
    """
