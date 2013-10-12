from django.conf.urls import patterns, url

urlpatterns = patterns('foo.views',
    # Listing URL
    url(r'^$', view='browse', name='foo.browse'),

    # Detail URL
    url(r'^(?P<slug>[\w\-\_\.\,]+)/$', view='detail', name='foo.detail'),
)
