"""
Testing Django REST Framework JWT token view for ska.
"""

import logging

import pytest
from constance import config
from django.test import TransactionTestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

import factories
from ska import sign_url
from ska.contrib.django.ska.settings import PROVIDERS, SECRET_KEY
from ska.defaults import DEFAULT_PROVIDER_PARAM

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = (
    "DRFIntegrationViewJwtTokenConstanceTestCase",
    "DRFIntegrationViewJwtTokenTestCase",
)

LOGGER = logging.getLogger(__name__)

OVERRIDE_SETTINGS_KWARGS = {
    "AUTHENTICATION_BACKENDS": (
        "ska.contrib.django.ska.backends.constance_backend."
        "SkaAuthenticationConstanceBackend",
        "django.contrib.auth.backends.ModelBackend",
    ),
    "ROOT_URLCONF": "constance_urls",
}


@pytest.mark.django_db
class BaseDRFIntegrationViewJwtTokenTestCase(TransactionTestCase):
    """Django REST framework integration view jwt token test case."""

    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        """Set up class."""
        cls.client = APIClient()

        cls.drf_obtain_jwt_token_url = reverse("ska.obtain_jwt_token")

        cls.AUTH_USER = "test_auth_backend_user"
        cls.AUTH_USER_EMAIL = "test_ska_auth_user@mail.example.com"
        cls.AUTH_USER_FIRST_NAME = "John"
        cls.AUTH_USER_LAST_NAME = "Doe"
        cls.PROVIDER_NAME = "client_1.admins"

    def setUp(self):
        """Set up."""
        factories.SkaSecretKeyConstanceFactory()
        factories.SkaProvidersConstanceFactory()

    def _test_obtain_jwt_token_request_not_signed_fail(self, url):
        """Fail test obtain JWT token request not signed.

        :return:
        """
        data = {}
        response = self.client.get(url, data)
        self.assertIn(
            response.status_code,
            (
                status.HTTP_401_UNAUTHORIZED,
                # status.HTTP_403_FORBIDDEN,
            ),
        )

    def _test_obtain_jwt_token_request_signed(
        self,
        secret_key,
        expected_response_code,
        url,
        auth_user=None,
        auth_user_email=None,
        provider_name=None,
        check_token=True,
        debug_info="",
    ):
        """Test obtain JWT token signed requests.

        :return:
        """
        if not auth_user:
            auth_user = self.AUTH_USER
        if not auth_user_email:
            auth_user_email = self.AUTH_USER_EMAIL

        # Testing signed URLs
        extra = {
            "email": auth_user_email,
            "first_name": self.AUTH_USER_FIRST_NAME,
            "last_name": self.AUTH_USER_LAST_NAME,
        }

        if provider_name:
            extra.update({DEFAULT_PROVIDER_PARAM: provider_name})

        signed_url = sign_url(
            auth_user=auth_user, secret_key=secret_key, url=url, extra=extra
        )

        data = {}

        if not isinstance(expected_response_code, (tuple, list)):
            expected_response_code = [expected_response_code]

        response = self.client.get(signed_url, data)

        self.assertIn(response.status_code, expected_response_code)
        if check_token:
            self.assertIn("token", response.data)


@pytest.mark.django_db
class DRFIntegrationViewJwtTokenTestCase(
    BaseDRFIntegrationViewJwtTokenTestCase
):
    """Django REST framework integration view JWT token test case."""

    pytestmark = pytest.mark.django_db

    # **************************************************************
    # ********************* Default permissions ********************
    # **************************************************************

    def test_obtain_jwt_token_request_not_signed_fail(self):
        """Fail test permissions provider list request not signed.

        :return:
        """
        self._test_obtain_jwt_token_request_not_signed_fail(
            self.drf_obtain_jwt_token_url
        )

    def test_obtain_jwt_token_provider_request_signed(self):
        """Test provider obtain JWT token signed request.

        :return:
        """
        secret_key = PROVIDERS[self.PROVIDER_NAME]["SECRET_KEY"]
        self._test_obtain_jwt_token_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.drf_obtain_jwt_token_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME,
        )

    def test_obtain_jwt_token_provider_request_signed_wrong_secret_key_fail(
        self,
    ):
        """Test provider obtains JWT token signed request wrong secret key.

        :return:
        """
        secret_key = PROVIDERS[self.PROVIDER_NAME]["SECRET_KEY"]
        self._test_obtain_jwt_token_request_signed(
            f"{secret_key}w",
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.drf_obtain_jwt_token_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME,
            check_token=False,
        )

    def test_obtain_jwt_token_request_signed(self):
        """Test obtain JWT token signed request.

        :return:
        """
        secret_key = SECRET_KEY
        self._test_obtain_jwt_token_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.drf_obtain_jwt_token_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
        )

    def test_obtain_jwt_token_request_signed_wrong_secret_key_fail(self):
        """Test obtain JWT token signed request wrong secret key.

        :return:
        """
        secret_key = SECRET_KEY
        self._test_obtain_jwt_token_request_signed(
            f"{secret_key}w",
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.drf_obtain_jwt_token_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            check_token=False,
        )


@pytest.mark.django_db
class DRFIntegrationViewJwtTokenConstanceTestCase(
    BaseDRFIntegrationViewJwtTokenTestCase
):
    """Django REST framework integration view JWT token constance test case."""

    pytestmark = pytest.mark.django_db

    # **************************************************************
    # ********************* Default permissions ********************
    # **************************************************************

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_obtain_jwt_token_request_not_signed_fail(self):
        """Fail test permissions provider list request not signed.

        :return:
        """
        self._test_obtain_jwt_token_request_not_signed_fail(
            self.drf_obtain_jwt_token_url
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_obtain_jwt_token_provider_request_signed(self):
        """Test provider obtain JWT token signed request.

        :return:
        """
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]["SECRET_KEY"]
        self._test_obtain_jwt_token_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.drf_obtain_jwt_token_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME,
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_obtain_jwt_token_provider_request_signed_wrong_secret_key_fail(
        self,
    ):
        """Test provider obtain JWT token signed request wrong secret key.

        :return:
        """
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]["SECRET_KEY"]
        self._test_obtain_jwt_token_request_signed(
            f"{secret_key}w",
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.drf_obtain_jwt_token_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            provider_name=self.PROVIDER_NAME,
            check_token=False,
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_obtain_jwt_token_request_signed(self):
        """Test obtain JWT token signed request.

        :return:
        """
        secret_key = config.SKA_SECRET_KEY
        self._test_obtain_jwt_token_request_signed(
            secret_key,
            status.HTTP_200_OK,
            self.drf_obtain_jwt_token_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
        )

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_obtain_jwt_token_request_signed_wrong_secret_key_fail(self):
        """Test obtain JWT token signed request wrong secret key.

        :return:
        """
        secret_key = config.SKA_SECRET_KEY
        self._test_obtain_jwt_token_request_signed(
            f"{secret_key}w",
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
            self.drf_obtain_jwt_token_url,
            auth_user=self.AUTH_USER,
            auth_user_email=self.AUTH_USER_EMAIL,
            check_token=False,
        )
