import json

from fake import (
    FACTORY,
    DjangoModelFactory,
)
from ska.versus import get_version

try:
    from constance.models import Constance  # noqa
except ImportError:
    from constance.backends.database.models import Constance  # noqa

__all__ = (
    "ConstanceFactory",
    "SkaProvidersConstanceFactory",
    "SkaSecretKeyConstanceFactory",
)

DJANGO_CONSTANCE_VERSION = get_version("django-constance")


SKA_PROVIDERS_VALUE = {
    # Client 1, group users
    "client_1.users": {
        "SECRET_KEY": "client-1-users-secret-key-constance",
    },
    # Client 1, group power_users
    "client_1.power_users": {
        "SECRET_KEY": "client-1-power-users-secret-key-constance",
        "USER_CREATE_CALLBACK": "foo.ska_callbacks."
        "client1_power_users_create",
    },
    # Client 1, group admins
    "client_1.admins": {
        "SECRET_KEY": "client-1-admins-secret-key-constance",
        "USER_CREATE_CALLBACK": "foo.ska_callbacks.client1_admins_create",
        "USER_GET_CALLBACK": "foo.ska_callbacks.client1_admins_get",
        "USER_INFO_CALLBACK": "foo.ska_callbacks."
        "client1_admins_info_constance",
        "REDIRECT_AFTER_LOGIN": "/admin/",
    },
}

SKA_SECRET_KEY_VALUE = "global-secret-key-constance"


class ConstanceFactory(DjangoModelFactory):
    key = FACTORY.word()
    value = FACTORY.text()

    class Meta:
        model = Constance
        get_or_create = ("key",)


class SkaProvidersConstanceFactory(DjangoModelFactory):
    key = "SKA_PROVIDERS"

    if DJANGO_CONSTANCE_VERSION.gte("4.0"):
        value = json.dumps(SKA_PROVIDERS_VALUE)
    else:
        value = SKA_PROVIDERS_VALUE

    class Meta:
        model = Constance
        get_or_create = ("key",)


class SkaSecretKeyConstanceFactory(DjangoModelFactory):
    """Ska secret key constance factory."""

    key = "SKA_SECRET_KEY"
    if DJANGO_CONSTANCE_VERSION.gte("4.0"):
        value = json.dumps(SKA_SECRET_KEY_VALUE)
    else:
        value = SKA_SECRET_KEY_VALUE

    class Meta:
        model = Constance
        get_or_create = ("key",)
