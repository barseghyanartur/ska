from nine import versions

from .views import FooDetailView, browse, authenticate, logged_in, detail

if versions.DJANGO_GTE_2_1:
    from django.urls import re_path as url
else:
    from django.conf.urls import url


urlpatterns = [
    # Listing URL
    url(r'^$', view=browse, name='foo.browse'),

    url(r'^authenticate/$', view=authenticate, name='foo.authenticate'),

    url(r'^logged-in/$', view=logged_in, name='foo.logged_in'),

    # Class based detail view URL
    url(r'^class-based/(?P<slug>[\w\-\_\.\,]+)/$', FooDetailView.as_view(),
        name='foo.class-based.detail'),

    # Detail URL
    url(r'^(?P<slug>[\w\-\_\.\,]+)/$', view=detail, name='foo.detail'),
]
