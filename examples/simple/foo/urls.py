from nine import versions

from rest_framework.routers import DefaultRouter

from .views import (
    FooDetailView,
    browse,
    authenticate,
    drf_permissions,
    logged_in,
    detail,
)
from .viewsets import FooItemViewSet

if versions.DJANGO_GTE_2_1:
    from django.urls import include, re_path as url
else:
    from django.conf.urls import include, url

router = DefaultRouter()

fooitems = router.register(
    r'fooitem',
    FooItemViewSet,
    base_name='fooitemmodel'
)

urlpatterns = [
    # Listing URL
    url(r'^$', view=browse, name='foo.browse'),

    url(r'^api/', include(router.urls)),

    url(r'^authenticate/$', view=authenticate, name='foo.authenticate'),

    url(r'^drf/$', view=drf_permissions, name='foo.drf_permissions'),

    url(r'^logged-in/$', view=logged_in, name='foo.logged_in'),

    # Class based detail view URL
    url(r'^class-based/(?P<slug>[\w\-\_\.\,]+)/$', FooDetailView.as_view(),
        name='foo.class-based.detail'),

    # Detail URL
    url(r'^(?P<slug>[\w\-\_\.\,]+)/$', view=detail, name='foo.detail'),
]
