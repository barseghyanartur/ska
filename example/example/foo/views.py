from django.http import Http404
from django.shortcuts import render_to_response
from django.template import RequestContext

from ska.contrib.django.ska.decorators import validate_signed_request

from foo.models import FooItem

def browse(request, template_name='foo/browse.html'):
    """
    Foo items listing.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    queryset = FooItem._default_manager.all().order_by('-date_published')

    context = {'items': queryset}

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
