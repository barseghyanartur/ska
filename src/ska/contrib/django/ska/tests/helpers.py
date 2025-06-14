import logging
import os
import random

import pytest

import factories

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = (
    "LOG_INFO",
    "NUM_ITEMS",
    "PROJECT_DIR",
    "SKA_TEST_USER_PASSWORD",
    "SKA_TEST_USER_USERNAME",
    "change_date",
    "create_admin_user",
    "generate_data",
    "log_info",
    "project_dir",
)

LOGGER = logging.getLogger(__name__)


def project_dir(base):
    """Project dir."""
    return os.path.join(os.path.dirname(__file__), base).replace("\\", "/")


PROJECT_DIR = project_dir

LOG_INFO = True

NUM_ITEMS = 5
SKA_TEST_USER_USERNAME = factories.TEST_ADMIN_USERNAME
SKA_TEST_USER_PASSWORD = factories.TEST_ADMIN_PASSWORD


def log_info(func):
    """Logs some useful info."""
    if not LOG_INFO:
        return func

    def inner(self, *args, **kwargs):
        """Inner."""
        result = func(self, *args, **kwargs)

        LOGGER.debug("\n\n%s", func.__name__)
        LOGGER.debug("============================")
        if func.__doc__:
            LOGGER.debug('""" %s """', func.__doc__.strip())
        LOGGER.debug("----------------------------")
        if result is not None:
            LOGGER.debug(result)
        LOGGER.debug("\n++++++++++++++++++++++++++++")

        return result

    return inner


def change_date():
    """Change date."""
    return bool(random.randint(0, 1))


@pytest.mark.django_db
def create_admin_user():
    """Create a user for testing the dashboard.

    TODO: At the moment an admin account is being tested. Automated tests
    with diverse accounts are to be implemented.
    """
    factories.UserFactory(
        email="admin@dev.django-ska.com",
        is_admin_user=True,
    )


@pytest.mark.django_db
def generate_data(num_items=NUM_ITEMS):
    """Generate data."""
    return factories.FooItemFactory.create_batch(num_items)
