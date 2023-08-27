from django.urls import re_path as url

from ..views import ObtainJSONWebTokenView

__author__ = "Artur Barseghyan"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("urlpatterns",)


urlpatterns = [
    url(
        r"^obtain-jwt-token/",
        ObtainJSONWebTokenView.as_view(),
        name="ska.obtain_jwt_token",
    ),
]
