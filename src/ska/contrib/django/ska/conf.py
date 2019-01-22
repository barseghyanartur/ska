from __future__ import absolute_import

from django.conf import settings

from ....contrib.django.ska import defaults

__title__ = 'ska.contrib.django.ska.conf'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('get_setting',)


def get_setting(setting, override=None):
    """Get a setting from `ska.contrib.django.ska` conf module, falling back
    to the default.

    If override is not None, it will be used instead of the setting.
    """
    attr_name = 'SKA_{}'.format(setting)
    if hasattr(settings, attr_name):
        return getattr(settings, attr_name)
    else:
        if hasattr(defaults, setting):
            return getattr(defaults, setting)
        else:
            return override
