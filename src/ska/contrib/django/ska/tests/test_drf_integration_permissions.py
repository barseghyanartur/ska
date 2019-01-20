"""
Testing Django REST Framework permissions for ska.
"""

import logging
import unittest

from constance import config
from django.test import TransactionTestCase, override_settings
import pytest
from rest_framework import status
from rest_framework.test import APIClient

from nine import versions

from ska import sign_url
from ska.contrib.django.ska.settings import SECRET_KEY, PROVIDERS
from ska.defaults import DEFAULT_PROVIDER_PARAM

import factories

if versions.DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'ska.contrib.django.ska.tests.test_drf_integration_permissions'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'DRFIntegrationPermissionsTestCase',
    'DRFIntegrationPermissionsConstanceTestCase',
)

LOGGER = logging.getLogger(__name__)

OVERRIDE_SETTINGS_KWARGS = {
    'AUTHENTICATION_BACKENDS': (
        'ska.contrib.django.ska.backends.constance_backend.'
        'SkaAuthenticationConstanceBackend',
        'django.contrib.auth.backends.ModelBackend',
    ),
    'ROOT_URLCONF': 'constance_urls',
}


@pytest.mark.django_db
class BaseDRFIntegrationPermissionsTestCase(TransactionTestCase):
    """Django REST framework integration permissions test case."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""

        cls.client = APIClient()

        cls.provider_list_url = reverse(
            'fooitemmodel_provider_signed_request_required-list'
        )
        cls.list_url = reverse(
            'fooitemmodel_signed_request_required-list'
        )

        cls.constance_provider_list_url = reverse(
            'fooitemmodel_constance_provider_signed_request_required-list'
        )
        cls.constance_list_url = reverse(
            'fooitemmodel_constance_signed_request_required-list'
        )

        cls.AUTH_USER = 'test_auth_backend_user'
        cls.AUTH_USER_EMAIL = 'test_ska_auth_user@mail.example.com'
        cls.AUTH_USER_FIRST_NAME = 'John'
        cls.AUTH_USER_LAST_NAME = 'Doe'
        cls.PROVIDER_NAME = 'client_1.admins'

    def setUp(self):
        """Set up."""
        self.foo_items = factories.FooItemFactory.create_batch(10)
        self.foo_item = self.foo_items[0]

        self.provider_detail_url = reverse(
            'fooitemmodel_provider_signed_request_required-detail',
            kwargs={'id': self.foo_item.pk}
        )
        self.detail_url = reverse(
            'fooitemmodel_signed_request_required-detail',
            kwargs={'id': self.foo_item.pk}
        )

        self.constance_provider_detail_url = reverse(
            'fooitemmodel_constance_provider_signed_request_required-detail',
            kwargs={'id': self.foo_item.pk}
        )
        self.constance_detail_url = reverse(
            'fooitemmodel_constance_signed_request_required-detail',
            kwargs={'id': self.foo_item.pk}
        )

        factories.SkaSecretKeyConstanceFactory()
        factories.SkaProvidersConstanceFactory()

    def _test_permissions_request_not_signed_fail(self, url):
        """Fail test permissions request not signed.

        :return:
        """
        data = {}
        response = self.client.get(url, data)
        self.assertIn(
            response.status_code,
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            )
        )

    def _test_permissions_request_signed(self,
                                         secret_key,
                                         expected_response_code,
                                         url,
                                         auth_user=None,
                                         auth_user_email=None,
                                         provider_name=None):
        """Test permissions signed requests.

        :return:
        """
        if not auth_user:
            auth_user = self.AUTH_USER
        if not auth_user_email:
            auth_user_email = self.AUTH_USER_EMAIL

        # Testing signed URLs
        extra = {
            'email': auth_user_email,
            'first_name': self.AUTH_USER_FIRST_NAME,
            'last_name': self.AUTH_USER_LAST_NAME,
        }

        if provider_name:
            extra.update({DEFAULT_PROVIDER_PARAM: provider_name})

        signed_list_url_url = sign_url(
            auth_user=auth_user,
            secret_key=secret_key,
            url=url,
            extra=extra
        )

        data = {}
        if not isinstance(expected_response_code, (tuple, list)):
            expected_response_code = [expected_response_code]
        response = self.client.get(signed_list_url_url, data)
        self.assertIn(response.status_code, expected_response_code)


@pytest.mark.django_db
class DRFIntegrationPermissionsTestCase(BaseDRFIntegrationPermissionsTestCase):
    """Django REST framework integration permissions test case."""

    pytestmark = pytest.mark.django_db

    # **************************************************************
    # ********************* Default permissions ********************
    # **************************************************************

    def test_permissions_provider_list_request_not_signed_fail(self):
        """Fail test permissions provider list request not signed.

        :return:
        """
        self._test_permissions_request_not_signed_fail(
            self.provider_list_url
        )

    def test_permissions_provider_detail_request_not_signed_fail(self):
        """Fail test permissions provider detail request not signed.

        :return:
        """
        self._test_permissions_request_not_signed_fail(
            self.provider_detail_url
        )

    def test_permissions_list_request_not_signed_fail(self):
        """Fail test permissions list request not signed.

        :return:
        """
        self._test_permissions_request_not_signed_fail(
            self.list_url
        )

    def test_permissions_detail_request_not_signed_fail(self):
        """Fail test permissions detail request not signed.

        :return:
        """
        self._test_permissions_request_not_signed_fail(
            self.detail_url
        )

    def test_provider_permissions_list_request_signed(self):
        """Test permissions signed provider list request.

        :return:
        """
        secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        self._test_permissions_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.provider_list_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME
        )

    def test_provider_permissions_detail_request_signed(self):
        """Test permissions signed provider detail request.

        :return:
        """
        secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        self._test_permissions_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.provider_detail_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME
        )

    def test_provider_permissions_list_request_signed_wrong_secret_key_fail(
            self
    ):
        """Test permissions signed provider list request wrong secret key.

        :return:
        """
        secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        self._test_permissions_request_signed(
            "{}w".format(secret_key),
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.provider_list_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME
        )

    def test_provider_permissions_detail_request_signed_wrong_secret_key_fail(
            self
    ):
        """Test permissions signed provider detail request wrong secret key.

        :return:
        """
        secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        self._test_permissions_request_signed(
            "{}w".format(secret_key),
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.provider_detail_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME
        )

    def test_permissions_list_request_signed(self):
        """Test permissions signed list request.

        :return:
        """
        secret_key = SECRET_KEY
        self._test_permissions_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.list_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL
        )

    def test_permissions_detail_request_signed(self):
        """Test permissions signed detail request.

        :return:
        """
        secret_key = SECRET_KEY
        self._test_permissions_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.detail_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL
        )

    def test_permissions_list_request_signed_wrong_secret_key_fail(self):
        """Test permissions signed list request wrong secret key.

        :return:
        """
        secret_key = SECRET_KEY
        self._test_permissions_request_signed(
            "{}w".format(secret_key),
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.list_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL
        )

    def test_permissions_detail_request_signed_wrong_secret_key_fail(self):
        """Test permissions signed detail request wrong secret key.

        :return:
        """
        secret_key = SECRET_KEY
        self._test_permissions_request_signed(
            "{}w".format(secret_key),
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.detail_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL
        )


@pytest.mark.django_db
class DRFIntegrationPermissionsConstanceTestCase(
    BaseDRFIntegrationPermissionsTestCase
):
    """Django REST framework integration permissions constance test case."""

    pytestmark = pytest.mark.django_db

    # **************************************************************
    # ********************* Default permissions ********************
    # **************************************************************

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_permissions_provider_list_request_not_signed_fail(self):
        """Fail test permissions provider list request not signed.

        :return:
        """
        self._test_permissions_request_not_signed_fail(
            self.constance_provider_list_url
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_permissions_provider_detail_request_not_signed_fail(self):
        """Fail test permissions provider detail request not signed.

        :return:
        """
        self._test_permissions_request_not_signed_fail(
            self.constance_provider_detail_url
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_permissions_list_request_not_signed_fail(self):
        """Fail test permissions list request not signed.

        :return:
        """
        self._test_permissions_request_not_signed_fail(
            self.constance_list_url
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_permissions_detail_request_not_signed_fail(self):
        """Fail test permissions detail request not signed.

        :return:
        """
        self._test_permissions_request_not_signed_fail(
            self.constance_detail_url
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_provider_permissions_list_request_signed(self):
        """Test permissions signed provider list request.

        :return:
        """
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        self._test_permissions_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.constance_provider_list_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_provider_permissions_detail_request_signed(self):
        """Test permissions signed provider detail request.

        :return:
        """
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        self._test_permissions_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.constance_provider_detail_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_provider_permissions_list_request_signed_wrong_secret_key_fail(
            self
    ):
        """Test permissions signed provider list request wrong secret key.

        :return:
        """
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        self._test_permissions_request_signed(
            "{}w".format(secret_key),
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.constance_provider_list_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_provider_permissions_detail_request_signed_wrong_secret_key_fail(
            self
    ):
        """Test permissions signed provider detail request wrong secret key.

        :return:
        """
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        self._test_permissions_request_signed(
            "{}w".format(secret_key),
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.constance_provider_detail_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_permissions_list_request_signed(self):
        """Test permissions signed list request.

        :return:
        """
        secret_key = config.SKA_SECRET_KEY
        self._test_permissions_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.constance_list_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_permissions_detail_request_signed(self):
        """Test permissions signed detail request.

        :return:
        """
        secret_key = config.SKA_SECRET_KEY
        self._test_permissions_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.constance_detail_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_permissions_list_request_signed_wrong_secret_key_fail(self):
        """Test permissions signed list request wrong secret key.

        :return:
        """
        secret_key = config.SKA_SECRET_KEY
        self._test_permissions_request_signed(
            "{}w".format(secret_key),
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.constance_list_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_permissions_detail_request_signed_wrong_secret_key_fail(self):
        """Test permissions signed detail request wrong secret key.

        :return:
        """
        secret_key = config.SKA_SECRET_KEY
        self._test_permissions_request_signed(
            "{}w".format(secret_key),
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.constance_detail_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL
        )


if __name__ == "__main__":
    # Tests
    unittest.main()
