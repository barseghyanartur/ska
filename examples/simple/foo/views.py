from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View
from django.urls import reverse

from ska import sign_url
from ska.contrib.django.ska.decorators import (
    validate_signed_request,
    m_validate_signed_request,
)
from ska.contrib.django.ska.settings import SECRET_KEY, PROVIDERS
from ska.defaults import DEFAULT_PROVIDER_PARAM

from foo.models import FooItem


def browse_view(request, template_name="foo/browse.html"):
    """Foo items listing.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    queryset = FooItem._default_manager.all()

    context = {"items": queryset}

    return render(request, template_name, context)


def authenticate_view(request, template_name="foo/authenticate.html"):
    """Authenticate.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    # Server ska login URL
    remote_ska_login_url = reverse("ska.login")

    # General login URLs
    remote_ska_login_urls = []
    for i in range(3):
        signed_remote_ska_login_url = sign_url(
            auth_user="test_ska_user_{0}".format(i),
            # Using general secret key
            secret_key=SECRET_KEY,
            url=remote_ska_login_url,
            extra={
                "email": "test_ska_user_{0}@mail.example.com".format(i),
                "first_name": "John {0}".format(i),
                "last_name": "Doe {0}".format(i),
            },
        )
        remote_ska_login_urls.append(
            (i, remote_ska_login_url, signed_remote_ska_login_url)
        )

    # Login URLs by provider
    remote_ska_login_urls_by_provider = []
    for uid, data in PROVIDERS.items():
        signed_remote_ska_login_url = sign_url(
            auth_user="test_ska_user_{0}".format(uid),
            # Using provider-specific secret key
            secret_key=data.get("SECRET_KEY"),
            url=remote_ska_login_url,
            extra={
                "email": "test_ska_user_{0}@mail.example.com".format(uid),
                "first_name": "John {0}".format(uid),
                "last_name": "Doe {0}".format(uid),
                DEFAULT_PROVIDER_PARAM: uid,
            },
        )
        remote_ska_login_urls_by_provider.append(
            (uid, remote_ska_login_url, signed_remote_ska_login_url)
        )

    # Fail-only login URLs by provider
    fail_only_remote_ska_login_urls_by_provider = []
    uid = "client_1.admins"
    data = PROVIDERS[uid]
    signed_remote_ska_login_url_invalid_username = sign_url(
        auth_user="forbidden_username",
        # Using provider-specific secret key
        secret_key=data.get("SECRET_KEY"),
        url=remote_ska_login_url,
        extra={
            "email": "test_ska_user_{0}@mail.example.com".format(uid),
            "first_name": "John {0}".format(uid),
            "last_name": "Doe {0}".format(uid),
            DEFAULT_PROVIDER_PARAM: uid,
        },
    )
    signed_remote_ska_login_url_invalid_email = sign_url(
        auth_user="test_ska_user_{0}".format(uid),
        # Using provider-specific secret key
        secret_key=data.get("SECRET_KEY"),
        url=remote_ska_login_url,
        extra={
            "email": "forbidden@example.com",
            "first_name": "John {0}".format(uid),
            "last_name": "Doe {0}".format(uid),
            DEFAULT_PROVIDER_PARAM: uid,
        },
    )
    fail_only_remote_ska_login_urls_by_provider.append(
        (
            uid,
            "invalid username: forbidden_username",
            signed_remote_ska_login_url_invalid_username,
        )
    )
    fail_only_remote_ska_login_urls_by_provider.append(
        (
            uid,
            "invalid email: forbidden@example.com",
            signed_remote_ska_login_url_invalid_email,
        )
    )

    # Template context
    context = {
        "remote_ska_login_urls": remote_ska_login_urls,
        "remote_ska_login_urls_by_provider": remote_ska_login_urls_by_provider,
        "fail_only_remote_ska_login_urls_by_provider": fail_only_remote_ska_login_urls_by_provider,
    }

    return render(request, template_name, context)


def drf_view(request, template_name="foo/drf.html"):
    """Django REST Framework permissions view.

    :param request:
    :param template_name:
    :return:
    """
    # *********************************************************
    # **************** Provider list URLS *********************
    # *********************************************************
    drf_remote_ska_provider_list_url = reverse(
        "fooitemmodel_provider_signed_request_required-list"
    )
    drf_remote_ska_list_urls_provider = []
    for uid, data in PROVIDERS.items():
        # Provider specific list URLs
        signed_remote_ska_login_url = sign_url(
            auth_user="test_ska_user_{0}".format(uid),
            # Using provider-specific secret key
            secret_key=data.get("SECRET_KEY"),
            url=drf_remote_ska_provider_list_url,
            extra={
                "email": "test_ska_user_{0}@mail.example.com".format(uid),
                "first_name": "John {0}".format(uid),
                "last_name": "Doe {0}".format(uid),
                DEFAULT_PROVIDER_PARAM: uid,
            },
        )
        drf_remote_ska_list_urls_provider.append(
            (
                uid,
                drf_remote_ska_provider_list_url,
                signed_remote_ska_login_url,
            )
        )

    # *********************************************************
    # *********************** List URLS ***********************
    # *********************************************************
    drf_remote_ska_list_url = reverse(
        "fooitemmodel_signed_request_required-list"
    )
    signed_remote_ska_login_url = sign_url(
        auth_user="test_ska_user",
        # Using global secret key
        secret_key=SECRET_KEY,
        url=drf_remote_ska_list_url,
        extra={
            "email": "test_ska_user@mail.example.com",
            "first_name": "John",
            "last_name": "Doe",
        },
    )
    drf_remote_ska_list_urls = [
        ("global", drf_remote_ska_list_url, signed_remote_ska_login_url)
    ]

    # *********************************************************
    # **************** Provider auth URLS *********************
    # *********************************************************
    drf_obtain_jwt_token_url = reverse("ska.obtain_jwt_token")
    drf_remote_ska_jwt_token_urls_provider = []
    for uid, data in PROVIDERS.items():
        # Provider specific list URLs
        _drf_signed_obtain_jwt_token_url = sign_url(
            auth_user="test_ska_user_{0}".format(uid),
            # Using provider-specific secret key
            secret_key=data.get("SECRET_KEY"),
            url=drf_obtain_jwt_token_url,
            extra={
                "email": "test_ska_user_{0}@mail.example.com".format(uid),
                "first_name": "John {0}".format(uid),
                "last_name": "Doe {0}".format(uid),
                DEFAULT_PROVIDER_PARAM: uid,
            },
        )
        drf_remote_ska_jwt_token_urls_provider.append(
            (
                uid,
                drf_obtain_jwt_token_url,
                _drf_signed_obtain_jwt_token_url,
            )
        )

    # *********************************************************
    # ***************** Global auth URLS **********************
    # *********************************************************
    drf_signed_obtain_jwt_token_url = sign_url(
        auth_user="test_ska_user",
        # Using global secret key
        secret_key=SECRET_KEY,
        url=drf_obtain_jwt_token_url,
        extra={
            "email": "test_ska_user@mail.example.com",
            "first_name": "John",
            "last_name": "Doe",
        },
    )
    drf_remote_ska_jwt_token_urls = [
        ("global", drf_obtain_jwt_token_url, drf_signed_obtain_jwt_token_url)
    ]

    # *********************************************************
    # ****************** Template context *********************
    # *********************************************************
    context = {
        "drf_remote_ska_list_urls": drf_remote_ska_list_urls,
        "drf_remote_ska_provider_list_url": drf_remote_ska_list_urls_provider,
        "drf_remote_ska_jwt_token_urls_provider": drf_remote_ska_jwt_token_urls_provider,
        "drf_remote_ska_jwt_token_urls": drf_remote_ska_jwt_token_urls,
    }

    return render(request, template_name, context)


@validate_signed_request()
def detail_view(request, slug, template_name="foo/detail.html"):
    """Foo item detail.

    :param django.http.HttpRequest request:
    :param str slug: Foo item slug.
    :param str template_name:
    :return django.http.HttpResponse:
    """
    try:
        item = FooItem._default_manager.get(slug=slug)
    except Exception as e:
        raise Http404

    context = {"item": item}

    return render(request, template_name, context)


class FooDetailView(View):
    """Class based view."""

    @m_validate_signed_request()
    def get(self, request, slug, template_name="foo/detail.html"):
        """Get."""
        try:
            item = FooItem._default_manager.get(slug=slug)
        except Exception as e:
            raise Http404

        context = {"item": item}

        return render(request, template_name, context)


def logged_in_view(request, template_name="foo/logged_in.html"):
    """Logged in landing page.

    :param django.http.HttpRequest request:
    :param str template_name:
    :return django.http.HttpResponse:
    """
    context = {}
    return render(request, template_name, context)
