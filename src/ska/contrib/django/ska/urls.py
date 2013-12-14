__title__ = 'ska.contrib.django.ska.urls'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('urlpatterns',)

from django.conf.urls import patterns, url

from ska.contrib.django.ska.views import login

urlpatterns = patterns('',
    url(r'^login/', login, name="ska.login"),
)
