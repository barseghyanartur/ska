from __future__ import absolute_import, print_function

import logging
import unittest

from django.test import Client, TransactionTestCase

import pytest

import factories

from .helpers import (
    generate_data,
    log_info,
    NUM_ITEMS,
)

__title__ = 'ska.contrib.django.ska.tests.test_decorators'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'SkaDecoratorsTest',
)

logger = logging.getLogger(__name__)


# *********************************************************************
# *********************************************************************
# *********************************************************************

SKA_TEST_USER_USERNAME = factories.TEST_ADMIN_USERNAME
SKA_TEST_USER_PASSWORD = factories.TEST_PASSWORD


@pytest.mark.django_db
class SkaDecoratorsTest(TransactionTestCase):
    """Testing model- and view- decorators."""

    pytestmark = pytest.mark.django_db

    def setUp(self):
        items = generate_data(NUM_ITEMS)

        # Testing the URLs
        self.item = items[0]

    @log_info
    def test_01_model_decorator(self):
        """Test the ``ska.contrib.django.ska.decorators.sign_url``."""
        # Testing signed URLs
        signed_absolute_url = self.item.get_signed_absolute_url()
        self.assertIsNotNone(signed_absolute_url)
        return signed_absolute_url

    @log_info
    def test_02_view_decorator_with_signed_url(self):
        """Test view decorator with signed URL.

        Test ``ska.contrib.django.ska.decorators.validate_signed_request``.
        """
        flow = []

        # Testing signed URLs
        signed_absolute_url = self.item.get_signed_absolute_url()
        self.assertIsNotNone(signed_absolute_url)
        flow.append(('Signed absolute URL', signed_absolute_url))

        # Testing view with signed URL
        client = Client()
        response = client.get(signed_absolute_url, {})
        response_status_code = getattr(response, 'status_code', None)
        self.assertIn(response_status_code, (200, 201, 202))
        flow.append(
            ('Response status code for signed URL', response_status_code)
        )

        return flow

    @log_info
    def test_03_view_decorator_with_unsigned_url(self):
        """Test view decorator with unsigned URL.

        Test the
        ``ska.contrib.django.ska.decorators.validate_signed_request`` view
        decorator with unsigned URL.
        """
        flow = []

        # Testing unsigned URLs
        absolute_url = self.item.get_absolute_url()
        self.assertTrue(absolute_url is not None)
        flow.append(('Unsigned absolute URL', absolute_url))

        # Testing view with signed URL
        client = Client()
        response = client.get(absolute_url, {})
        response_status_code = getattr(response, 'status_code', None)
        response_content = getattr(response, 'content', "")
        self.assertIn(response_status_code, (401,))
        flow.append(
            ('Response status code for unsigned URL', response_status_code)
        )
        flow.append(
            ('Response content for unsigned URL', response_content)
        )

        return flow

    @log_info
    def test_04_class_based_view_decorator_with_signed_url(self):
        """Test class based view decorator with signed URL.

        Test ``ska.contrib.django.ska.decorators.validate_signed_request``.
        """
        flow = []

        # Testing signed URLs
        signed_absolute_url = self.item \
            .get_signed_class_based_absolute_url()
        self.assertIsNotNone(signed_absolute_url)
        flow.append(('Signed absolute URL', signed_absolute_url))

        # Testing view with signed URL
        client = Client()
        response = client.get(signed_absolute_url, {})
        response_status_code = getattr(response, 'status_code', None)
        self.assertIn(response_status_code, (200, 201, 202))
        flow.append(
            ('Response status code for signed URL', response_status_code)
        )

        return flow

    @log_info
    def test_05_class_based_view_decorator_with_unsigned_url(self):
        """Test class based view decorator with unsigned URL.

        Test the
        ``ska.contrib.django.ska.decorators.validate_signed_request`` view
        decorator with unsigned URL.
        """
        flow = []

        # Testing unsigned URLs
        absolute_url = self.item.get_cbv_absolute_url()
        self.assertTrue(absolute_url is not None)
        flow.append(('Unsigned absolute URL', absolute_url))

        # Testing view with signed URL
        client = Client()
        response = client.get(absolute_url, {})
        response_status_code = getattr(response, 'status_code', None)
        response_content = getattr(response, 'content', "")
        self.assertIn(response_status_code, (401,))
        flow.append(
            ('Response status code for unsigned URL', response_status_code)
        )
        flow.append(
            ('Response content for unsigned URL', response_content)
        )

        return flow


if __name__ == "__main__":
    # Tests
    unittest.main()
