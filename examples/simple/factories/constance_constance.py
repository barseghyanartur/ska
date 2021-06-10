import json

from factory import DjangoModelFactory

from constance.backends.database.models import Constance

from .factory_faker import Faker

__all__ = (
    "ConstanceFactory",
    "SkaProvidersConstanceFactory",
    "SkaSecretKeyConstanceFactory",
)


class BaseConstanceFactory(DjangoModelFactory):
    """Base Constance factory."""

    key = Faker("word")
    value = Faker("text")

    class Meta(object):
        """Meta class."""

        model = Constance
        abstract = True
        django_get_or_create = ("key",)


class ConstanceFactory(BaseConstanceFactory):
    """Constance factory."""


class SkaProvidersConstanceFactory(ConstanceFactory):
    """Ska providers constance factory."""

    key = "SKA_PROVIDERS"
    value = {
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

    class Meta(object):
        """Meta class."""

        django_get_or_create = ("key",)


class SkaSecretKeyConstanceFactory(ConstanceFactory):
    """Ska secret key constance factory."""

    key = "SKA_SECRET_KEY"
    value = "global-secret-key-constance"

    class Meta(object):
        """Meta class."""

        django_get_or_create = ("key",)
