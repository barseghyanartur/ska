from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.base import View
from django.core.urlresolvers import reverse

from ska import sign_url
from ska.contrib.django.ska.decorators import validate_signed_request, m_validate_signed_request
from ska.contrib.django.ska.settings import SECRET_KEY

from foo.models import FooItem

def browse(request, template_name='foo/browse.html'):
    """
    Foo items listing.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    queryset = FooItem._default_manager.all()

    context = {
        'items': queryset,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))

def authenticate(request, template_name='foo/authenticate.html'):
    """
    Authenticate.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    remote_ska_login_urls = []

    for i in range(10):
        remote_ska_login_url = reverse('ska.login')
        signed_remote_ska_login_url = sign_url(
            auth_user = 'test_ska_user_{0}'.format(i),
            secret_key = SECRET_KEY,
            url = remote_ska_login_url
            )
        remote_ska_login_urls.append((remote_ska_login_url, signed_remote_ska_login_url))

    context = {
        'remote_ska_login_urls': remote_ska_login_urls,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))

@validate_signed_request()
def detail(request, slug, template_name='foo/detail.html'):
    """
    Foo item detail.

    :param django.http.HttpRequest request:
    :param str slug: Foo item slug.
    :param str template_name:
    :return django.http.HttpResponse:
    """
    try:
        item = FooItem._default_manager.get(slug=slug)
    except Exception as e:
        raise Http404

    context = {'item': item}

    return render_to_response(template_name, context, context_instance=RequestContext(request))

class FooDetailView(View):
    """
    Class based view.
    """
    @m_validate_signed_request()
    def get(self, request, slug, template_name='foo/detail.html'):
        try:
            item = FooItem._default_manager.get(slug=slug)
        except Exception as e:
            raise Http404

        context = {'item': item}

        return render_to_response(template_name, context, context_instance=RequestContext(request))

def logged_in(request, template_name='foo/logged_in.html'):
    """
    Logged in landing page.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    context = {}
    return render_to_response(template_name, context, context_instance=RequestContext(request))
