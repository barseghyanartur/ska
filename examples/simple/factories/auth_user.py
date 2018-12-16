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

__all__ = (
    'AbstractUserFactory',
    'InactiveUserFactory',
    'LimitedUserFactory',
    'StaffUserFactory',
    'SuperAdminUserFactory',
    'SuperuserUserFactory',
    'TEST_PASSWORD',
    'TEST_USERNAME',
    'TEST_ADMIN_USERNAME',
    'TestAdminUsernameSuperAdminUserFactory',
    'TestUsernameUserFactory',
    'UserFactory',
)

# Simple admin roles, nothing to do with workflow
TEST_USERNAME = 'test_user'
TEST_ADMIN_USERNAME = 'test_admin'
TEST_PASSWORD = 'test_password'

FAKER = OriginalFaker()


class AbstractUserFactory(DjangoModelFactory):
    """Abstract factory for creating users."""

    password = PostGenerationMethodCall('set_password', TEST_PASSWORD)
    username = Sequence(lambda n: 'user%d' % n)
    first_name = Faker('first_name_max_length_30')
    last_name = Faker('last_name_max_length_30')
    email = Faker('ascii_safe_email')

    is_active = False
    is_staff = False
    is_superuser = False

    class Meta(object):
        """Meta options."""

        model = settings.AUTH_USER_MODEL
        django_get_or_create = ('username',)
        abstract = True


class InactiveUserFactory(AbstractUserFactory):
    """Factory for creating inactive users.

    No roles. Incomplete MFA setup.
    """


class UserFactory(AbstractUserFactory):
    """Factory for creating active users.

    No roles. Incomplete MFA setup.
    """

    is_active = True


class StaffUserFactory(UserFactory):
    """Factory for creating staff (admin) users.

    No roles. Incomplete MFA setup.
    """

    is_staff = True


class SuperuserUserFactory(UserFactory):
    """Factory for creating superuser users.

    No roles. Incomplete MFA setup.
    """

    is_superuser = True


class SuperAdminUserFactory(UserFactory):
    """Factory for creating super admin users.

    No roles. Incomplete MFA setup.
    """

    is_staff = True
    is_superuser = True


class TestAdminUsernameSuperAdminUserFactory(UserFactory):
    """Factory for creating super admin user test_admin.

    No roles. Incomplete MFA setup.
    """

    username = TEST_ADMIN_USERNAME
    is_staff = True
    is_superuser = True


class TestUsernameUserFactory(UserFactory):
    """Factory for creating user test_user.

    No roles. Incomplete MFA setup.
    """

    username = TEST_USERNAME


class LimitedUserFactory(UserFactory):
    """User factory, but limited to 20 users.

    No roles. Incomplete MFA setup.
    """

    id = LazyAttribute(
        lambda __x: random.randint(1, 20)
    )

    class Meta(object):
        """Meta class."""

        django_get_or_create = ('id',)
