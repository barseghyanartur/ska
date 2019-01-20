from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from nine import versions

if versions.DJANGO_GTE_2_1:
    from django.urls import include, re_path as url
else:
    from django.conf.urls import url, include

admin.autodiscover()

urlpatterns = []

if versions.DJANGO_GTE_2_0:
    urlpatterns += [
        url(r'^admin/', admin.site.urls),
    ]
else:
    urlpatterns += [
        url(r'^admin/', include(admin.site.urls)),
    ]

urlpatterns += [
    url(r'^ska/', include('ska.contrib.django.ska.urls')),
    url(
        r'^ska-rest/',
        include('ska.contrib.django.ska.integration.drf.urls.jwt_token')
    ),
    url(r'^foo/', include('foo.urls')),
    url(r'^$', TemplateView.as_view(template_name='home.html')),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
