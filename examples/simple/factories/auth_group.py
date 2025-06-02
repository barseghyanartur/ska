from django.contrib.auth.models import Group
from fake import (
    FACTORY,
    DjangoModelFactory,
)

__all__ = (
    "GroupFactory",
)


class GroupFactory(DjangoModelFactory):
    """Group factory."""

    name = FACTORY.word()

    class Meta:
        model = Group
        get_or_create = ("name",)
