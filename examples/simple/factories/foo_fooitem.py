from fake import (
    FACTORY,
    DjangoModelFactory,
)

from foo.models import FooItem

__all__ = ("FooItemFactory",)


class FooItemFactory(DjangoModelFactory):
    title = FACTORY.sentence()
    slug = FACTORY.slug()
    body = FACTORY.text()

    class Meta:
        model = FooItem
        get_or_create = ("title",)
