from django.apps import AppConfig

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("Config",)


class Config(AppConfig):
    """Config."""

    name = "ska.contrib.django.ska"
    # label = 'ska_contrib_django_ska'
    label = "ska"
