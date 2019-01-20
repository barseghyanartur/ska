from __future__ import absolute_import

from nine import versions

from ..views import ObtainJSONWebTokenView

if versions.DJANGO_GTE_2_1:
    from django.urls import re_path as url
else:
    from django.conf.urls import url


__title__ = 'ska.contrib.django.ska.integration.drf.urls.jwt_token'
__author__ = 'Artur Barseghyan'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('urlpatterns',)


urlpatterns = [
    url(
        r'^obtain-jwt-token/',
        ObtainJSONWebTokenView.as_view(),
        name="ska.obtain_jwt_token"
    ),
]
