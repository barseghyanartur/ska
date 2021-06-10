import random

from django.contrib.auth.models import Group

from factory import (
    DjangoModelFactory,
    LazyAttribute,
)
from faker import Faker as OriginalFaker

from .factory_faker import Faker

__all__ = (
    "AbstractGroupFactory",
    "GroupFactory",
    "LimitedGroupFactory",
)

FAKER = OriginalFaker()


class AbstractGroupFactory(DjangoModelFactory):
    """Abstract factory for creating groups."""

    name = Faker("word")

    class Meta(object):
        """Meta options."""

        model = Group
        django_get_or_create = ("name",)
        abstract = True


class GroupFactory(AbstractGroupFactory):
    """Factory for creating active groups."""


class LimitedGroupFactory(GroupFactory):
    """User factory, but limited to 20 group."""

    id = LazyAttribute(lambda __x: random.randint(1, 5))

    class Meta(object):
        """Meta class."""

        django_get_or_create = ("id",)
