from __future__ import absolute_import

from django import template
from django.core.exceptions import ImproperlyConfigured

from constance import config

from ..... import sign_url as ska_sign_url
from .....defaults import (
    DEFAULT_AUTH_USER_PARAM,
    DEFAULT_EXTRA_PARAM,
    DEFAULT_PROVIDER_PARAM,
    DEFAULT_SIGNATURE_PARAM,
    DEFAULT_URL_SUFFIX,
    DEFAULT_VALID_UNTIL_PARAM,
    SIGNATURE_LIFETIME,
)
from .....signatures import Signature

__title__ = 'ska.contrib.django.ska.templatetags.ska_constance_tags'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'sign_url',
    'provider_sign_url',
)


register = template.Library()


@register.simple_tag(takes_context=True)
def sign_url(context,
             url='',
             auth_user=None,
             valid_until=None,
             lifetime=SIGNATURE_LIFETIME,
             suffix=DEFAULT_URL_SUFFIX,
             signature_param=DEFAULT_SIGNATURE_PARAM,
             auth_user_param=DEFAULT_AUTH_USER_PARAM,
             valid_until_param=DEFAULT_VALID_UNTIL_PARAM,
             extra=None,
             extra_param=DEFAULT_EXTRA_PARAM,
             signature_cls=Signature):
    """Sign URL."""
    # The `extra` and `extra_param` are not used at the moment.
    if not auth_user:
        auth_user = context['request'].user.get_username()

    secret_key = config.SKA_SECRET_KEY

    return ska_sign_url(
        auth_user=auth_user,
        secret_key=secret_key,
        valid_until=valid_until,
        lifetime=lifetime,
        url=url,
        suffix=suffix,
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra=extra,
        extra_param=extra_param,
        signature_cls=signature_cls
    )


@register.simple_tag(takes_context=True)
def provider_sign_url(context,
                      provider,
                      url='',
                      auth_user=None,
                      valid_until=None,
                      lifetime=SIGNATURE_LIFETIME,
                      suffix=DEFAULT_URL_SUFFIX,
                      signature_param=DEFAULT_SIGNATURE_PARAM,
                      auth_user_param=DEFAULT_AUTH_USER_PARAM,
                      valid_until_param=DEFAULT_VALID_UNTIL_PARAM,
                      extra=None,
                      extra_param=DEFAULT_EXTRA_PARAM,
                      signature_cls=Signature,
                      fail_silently=True):
    """Sign URL."""
    # The `extra` and `extra_param` are not used at the moment.
    if not auth_user:
        auth_user = context['request'].user.get_username()

    if provider not in config.SKA_PROVIDERS:
        if fail_silently:
            return None
        else:
            raise ImproperlyConfigured(
                "Provider {} does not exist".format(provider)
            )
    secret_key = config.SKA_PROVIDERS.get(provider, {}).get('SECRET_KEY', None)

    if extra is None:
        extra = {}

    extra.update({DEFAULT_PROVIDER_PARAM: provider})

    return ska_sign_url(
        auth_user=auth_user,
        secret_key=secret_key,
        valid_until=valid_until,
        lifetime=lifetime,
        url=url,
        suffix=suffix,
        signature_param=signature_param,
        auth_user_param=auth_user_param,
        valid_until_param=valid_until_param,
        extra=extra,
        extra_param=extra_param,
        signature_cls=signature_cls
    )
