from __future__ import absolute_import

__title__ = 'ska.contrib.django.ska.conf'
__version__ = '0.9'
__build__ = 0x000009
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__all__ = ('get_setting',)

from django.conf import settings

from ska.contrib.django.ska import defaults

def get_setting(setting, override=None):
    """
    Get a setting from `ska.contrib.django.ska` conf module, falling back to the default.

    If override is not None, it will be used instead of the setting.
    """
    if override is not None:
        return override
    if hasattr(settings, 'SKA_%s' % setting):
        return getattr(settings, 'SKA_%s' % setting)
    else:
        return getattr(defaults, setting)
