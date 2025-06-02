from django.contrib.auth.models import User
from fake import (
    FACTORY,
    DjangoModelFactory,
    PostSave,
    PreSave,
    trait,
)

from .auth_group import GroupFactory

__all__ = (
    "UserFactory",
    "TEST_ADMIN_USERNAME",
    "TEST_ADMIN_PASSWORD",
)

TEST_ADMIN_USERNAME = "test_admin"
TEST_ADMIN_PASSWORD = "test_password"


def set_password(user: User, password: str) -> None:
    """Helper function for setting password for the User."""
    user.set_password(password)


def add_to_group(user: User, name: str) -> None:
    """Helper function for adding the User to a Group."""
    group = GroupFactory(name=name)
    user.groups.add(group)


class UserFactory(DjangoModelFactory):
    """User factory."""

    username = FACTORY.username()
    first_name = FACTORY.first_name()
    last_name = FACTORY.last_name()
    email = FACTORY.email()
    date_joined = FACTORY.date_time()
    last_login = FACTORY.date_time()
    is_superuser = False
    is_staff = False
    is_active = FACTORY.pybool()
    password = PreSave(set_password, password=TEST_ADMIN_PASSWORD)
    group = PostSave(add_to_group, name="Test group")

    class Meta:
        model = User
        get_or_create = ("username",)

    @trait
    def is_admin_user(self, instance: User) -> None:
        """Trait."""
        instance.is_superuser = True
        instance.is_staff = True
        instance.is_active = True
        instance.username = TEST_ADMIN_USERNAME
