from __future__ import absolute_import

from django import template

from ..... import sign_url as ska_sign_url
from .....defaults import (
    SIGNATURE_LIFETIME,
    DEFAULT_URL_SUFFIX,
    DEFAULT_SIGNATURE_PARAM,
    DEFAULT_AUTH_USER_PARAM,
    DEFAULT_VALID_UNTIL_PARAM,
    DEFAULT_EXTRA_PARAM
)
from .....signatures import Signature
from ..settings import SECRET_KEY

__title__ = 'ska.contrib.django.ska.templatetags.ska_tags'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2016 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('sign_url',)


register = template.Library()


@register.assignment_tag(takes_context=True)
def sign_url(context,
             url='',
             auth_user=None,
             secret_key=SECRET_KEY,
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
