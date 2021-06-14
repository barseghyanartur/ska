from typing import Optional, Type, Dict, Union

from django import template
from django.core.exceptions import ImproperlyConfigured
from django.template import RequestContext

from ..... import sign_url as ska_sign_url
from .....base import AbstractSignature
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
from ..settings import SECRET_KEY, PROVIDERS


__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = (
    "sign_url",
    "provider_sign_url",
)


register = template.Library()


@register.simple_tag(takes_context=True)
def sign_url(
    context: RequestContext,
    url: str = "",
    auth_user: Optional[str] = None,
    secret_key: str = SECRET_KEY,
    valid_until: Optional[Union[float, str]] = None,
    lifetime: int = SIGNATURE_LIFETIME,
    suffix: str = DEFAULT_URL_SUFFIX,
    signature_param: str = DEFAULT_SIGNATURE_PARAM,
    auth_user_param: str = DEFAULT_AUTH_USER_PARAM,
    valid_until_param: str = DEFAULT_VALID_UNTIL_PARAM,
    extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
    extra_param: str = DEFAULT_EXTRA_PARAM,
    signature_cls: Type[AbstractSignature] = Signature,
) -> str:
    """Sign URL."""
    # The `extra` and `extra_param` are not used at the moment.
    if not auth_user:
        auth_user = context["request"].user.get_username()

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
        signature_cls=signature_cls,
    )


@register.simple_tag(takes_context=True)
def provider_sign_url(
    context: RequestContext,
    provider: str,
    url: str = "",
    auth_user: Optional[str] = None,
    valid_until: Optional[Union[float, str]] = None,
    lifetime: int = SIGNATURE_LIFETIME,
    suffix: str = DEFAULT_URL_SUFFIX,
    signature_param: str = DEFAULT_SIGNATURE_PARAM,
    auth_user_param: str = DEFAULT_AUTH_USER_PARAM,
    valid_until_param: str = DEFAULT_VALID_UNTIL_PARAM,
    extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
    extra_param: str = DEFAULT_EXTRA_PARAM,
    signature_cls: Type[AbstractSignature] = Signature,
    fail_silently: bool = True,
) -> Union[str, None]:
    """Sign URL."""
    # The `extra` and `extra_param` are not used at the moment.
    if not auth_user:
        auth_user = context["request"].user.get_username()

    if provider not in PROVIDERS:
        if fail_silently:
            return None
        else:
            raise ImproperlyConfigured(f"Provider {provider} does not exist")
    secret_key = PROVIDERS.get(provider, {}).get("SECRET_KEY", None)

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
        signature_cls=signature_cls,
    )
