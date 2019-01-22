from __future__ import absolute_import
from django.apps import AppConfig

__title__ = 'ska.contrib.django.ska.apps'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('Config',)


class Config(AppConfig):
    """Config."""

    name = 'ska.contrib.django.ska'
    # label = 'ska_contrib_django_ska'
    label = 'ska'
