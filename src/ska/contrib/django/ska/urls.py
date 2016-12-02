from __future__ import absolute_import

from django.conf.urls import url

from .views import login

__title__ = 'ska.contrib.django.ska.urls'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('urlpatterns',)


urlpatterns = [
    url(r'^login/', login, name="ska.login"),
]
