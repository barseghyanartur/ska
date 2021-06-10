import random

from django.conf import settings

from factory import (
    DjangoModelFactory,
    PostGenerationMethodCall,
    Sequence,
    post_generation,
    LazyAttribute,
)
from faker import Faker as OriginalFaker
from factory import SubFactory

from .factory_faker import Faker
from .auth_group import LimitedGroupFactory

__all__ = (
    "AbstractUserFactory",
    "InactiveUserFactory",
    "LimitedUserFactory",
    "StaffUserFactory",
    "SuperAdminUserFactory",
    "SuperuserUserFactory",
    "TEST_PASSWORD",
    "TEST_USERNAME",
    "TEST_ADMIN_USERNAME",
    "TestAdminUsernameSuperAdminUserFactory",
    "TestUsernameUserFactory",
    "UserFactory",
)

# Simple admin roles, nothing to do with workflow
TEST_USERNAME = "test_user"
TEST_ADMIN_USERNAME = "test_admin"
TEST_PASSWORD = "test_password"

FAKER = OriginalFaker()


class AbstractUserFactory(DjangoModelFactory):
    """Abstract factory for creating users."""

    password = PostGenerationMethodCall("set_password", TEST_PASSWORD)
    username = Sequence(lambda n: "user%d" % n)
    first_name = Faker("first_name")
    last_name = Faker("last_name")
    # first_name = Faker('first_name_max_length_30')
    # last_name = Faker('last_name_max_length_30')
    email = Faker("ascii_safe_email")

    is_active = False
    is_staff = False
    is_superuser = False

    class Meta(object):
        """Meta options."""

        model = settings.AUTH_USER_MODEL
        django_get_or_create = ("username",)
        abstract = True

    @post_generation
    def groups(obj, created, extracted, **kwargs):
        """Create Group objects for the created User instance."""
        if created:
            # Create from 1 to 7 ``Group`` objects.
            amount = random.randint(1, 5)
            groups = LimitedGroupFactory.create_batch(amount)
            obj.groups.add(*groups)


class InactiveUserFactory(AbstractUserFactory):
    """Factory for creating inactive users."""


class UserFactory(AbstractUserFactory):
    """Factory for creating active users."""

    is_active = True


class StaffUserFactory(UserFactory):
    """Factory for creating staff (admin) users."""

    is_staff = True


class SuperuserUserFactory(UserFactory):
    """Factory for creating superuser users."""

    is_superuser = True


class SuperAdminUserFactory(UserFactory):
    """Factory for creating super admin users."""

    is_staff = True
    is_superuser = True


class TestAdminUsernameSuperAdminUserFactory(UserFactory):
    """Factory for creating super admin user test_admin."""

    username = TEST_ADMIN_USERNAME
    is_staff = True
    is_superuser = True


class TestUsernameUserFactory(UserFactory):
    """Factory for creating user test_user."""

    username = TEST_USERNAME


class LimitedUserFactory(UserFactory):
    """User factory, but limited to 20 users."""

    id = LazyAttribute(lambda __x: random.randint(1, 20))

    class Meta(object):
        """Meta class."""

        django_get_or_create = ("id",)
