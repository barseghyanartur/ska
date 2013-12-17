from django.conf.urls import patterns, url

from foo.views import FooDetailView

urlpatterns = patterns('foo.views',
    # Listing URL
    url(r'^$', view='browse', name='foo.browse'),

    url(r'^authenticate/$', view='authenticate', name='foo.authenticate'),

    url(r'^logged-in/$', view='logged_in', name='foo.logged_in'),

    # Class based detail view URL
    url(r'^class-based/(?P<slug>[\w\-\_\.\,]+)/$', FooDetailView.as_view(),
        name='foo.class-based.detail'),

    # Detail URL
    url(r'^(?P<slug>[\w\-\_\.\,]+)/$', view='detail', name='foo.detail'),
)
