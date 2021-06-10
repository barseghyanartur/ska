import random

from django.utils.text import slugify

from factory import DjangoModelFactory, LazyAttribute
from factory.fuzzy import FuzzyChoice

from foo.models import FooItem

from .factory_faker import Faker

__all__ = (
    "FooItemFactory",
    "LimitedFooItemFactory",
)


class BaseFooItemFactory(DjangoModelFactory):
    """Base FooItem factory."""

    title = Faker("text", max_nb_chars=100)
    slug = LazyAttribute(lambda obj: slugify(obj.title))
    body = Faker("text")

    class Meta(object):
        """Meta class."""

        model = FooItem
        abstract = True
        django_get_or_create = ("title",)


class FooItemFactory(BaseFooItemFactory):
    """FooItem factory."""


class LimitedFooItemFactory(BaseFooItemFactory):
    """FooItem factory, but limited to 20 records."""

    id = LazyAttribute(lambda __x: random.randint(1, 20))

    class Meta(object):
        """Meta class."""

        django_get_or_create = ("id",)
