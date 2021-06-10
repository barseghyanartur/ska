from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, re_path as url
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = []

urlpatterns += [
    url(r"^admin/", admin.site.urls),
]

urlpatterns += [
    url(r"^ska/", include("ska.contrib.django.ska.urls.constance_urls")),
    url(
        r"^ska-rest/",
        include("ska.contrib.django.ska.integration.drf.urls.jwt_token"),
    ),
    url(r"^foo/", include("foo.urls")),
    url(
        r"^templatetags$",
        TemplateView.as_view(template_name="foo/constance_templatetags.html"),
        name="foo.templatetags",
    ),
    url(r"^$", TemplateView.as_view(template_name="home.html")),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
