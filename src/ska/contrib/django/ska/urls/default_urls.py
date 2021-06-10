from django.urls import re_path as url

from ..views import login

__author__ = "Artur Barseghyan"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("urlpatterns",)


urlpatterns = [
    url(r"^login/", login, name="ska.login"),
]
