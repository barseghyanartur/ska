from __future__ import absolute_import, print_function

import datetime
import logging
import time
import unittest

from django.core import mail
from django.core.management import call_command
from django.test import Client, TransactionTestCase, override_settings

import mock

import pytest

from ska import sign_url
from ska.contrib.django.ska.models import Signature
from ska.contrib.django.ska import settings as ska_settings
from ska.defaults import DEFAULT_PROVIDER_PARAM

import factories

from .helpers import log_info

__title__ = 'ska.contrib.django.ska.tests.test_default_authentication_backend'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'SkaAuthenticationBackendTest',
)

logger = logging.getLogger(__name__)


OVERRIDE_SETTINGS_DB_STORE_SIGNATURES_KWARGS = {
    'SKA_DB_STORE_SIGNATURES': True,
    'SKA_DB_PERFORM_SIGNATURE_CHECK': True,
}

# *********************************************************************
# *********************************************************************
# *********************************************************************

SKA_TEST_USER_USERNAME = factories.TEST_ADMIN_USERNAME
SKA_TEST_USER_PASSWORD = factories.TEST_PASSWORD


@pytest.mark.django_db
class SkaAuthenticationBackendTest(TransactionTestCase):
    """Tests for auth backend."""

    pytestmark = pytest.mark.django_db

    def setUp(self):
        self.AUTH_USER = 'test_auth_backend_user'
        self.AUTH_USER_EMAIL = 'test_ska_auth_user@mail.example.com'
        self.AUTH_USER_FIRST_NAME = 'John'
        self.AUTH_USER_LAST_NAME = 'Doe'
        self.PROVIDER_NAME = 'client_1.admins'
        self.LOGIN_URL = '/ska/login/'

    def __test_login(self,
                     secret_key,
                     response_codes,
                     provider_name=None,
                     logout=False,
                     test_email_data=None,
                     do_signature_check=True,
                     auth_user=None,
                     auth_user_email=None,
                     debug_info=""):
        """Test login.

        :param secret_key:
        :param response_codes: First response code is used
        :param provider_name:
        :param logout:
        :param test_email_data:
        :param do_signature_check: It's a tuple. The second code is
            used only if both `DB_STORE_SIGNATURES` and
            `DB_PERFORM_SIGNATURE_CHECK` values are True, which means
            that users can't use same signatures twice.
        :param auth_user:
        :param auth_user_email:
        :return:
        """
        flow = []

        if not auth_user:
            auth_user = self.AUTH_USER
        if not auth_user_email:
            auth_user_email = self.AUTH_USER_EMAIL

        first_response_code, second_response_code = response_codes

        # Testing signed URLs
        extra = {
            'email': auth_user_email,
            'first_name': self.AUTH_USER_FIRST_NAME,
            'last_name': self.AUTH_USER_LAST_NAME,
        }
        if provider_name:
            extra.update({DEFAULT_PROVIDER_PARAM: provider_name})

        signed_login_url = sign_url(
            auth_user=auth_user,
            secret_key=secret_key,
            url=self.LOGIN_URL,
            extra=extra
        )

        self.assertIsNotNone(signed_login_url)
        flow.append(('Signed login URL', signed_login_url))

        # Testing view with signed URL
        self._client = Client()
        response = self._client.get(signed_login_url, {})
        response_status_code = getattr(response, 'status_code', None)

        self.assertIn(response_status_code, (first_response_code,))
        flow.append(
            (
                'Response status code for signed URL',
                response_status_code
            )
        )

        if test_email_data:
            self.assertEqual(
                len(mail.outbox),
                len(test_email_data['emails'])
            )

            for _index, _subject in test_email_data['emails'].items():
                self.assertEqual(
                    mail.outbox[_index].subject,
                    _subject
                )

        if logout:
            self.__logout()

        # If both `DB_STORE_SIGNATURES` and `DB_PERFORM_SIGNATURE_CHECK`
        # are set to True, second login attempt shall not be successful.
        if ska_settings.DB_STORE_SIGNATURES \
                and ska_settings.DB_PERFORM_SIGNATURE_CHECK \
                and do_signature_check:
            # Testing again with signed URL and this time, it should fail

            self._client = Client()
            response = self._client.get(signed_login_url, {})
            response_status_code = getattr(response, 'status_code', None)
            self.assertIn(response_status_code, (second_response_code,))
            flow.append(
                (
                    'Response status '
                    'code for signed URL', response_status_code
                )
            )
            if logout:
                self.__logout()

        return flow

    def __logout(self):
        """Log out."""
        self._client.logout()

    @log_info
    def test_01_login(self):
        """Test auth using general ``SECRET_KEY``."""
        return self.__test_login(
            ska_settings.SECRET_KEY,
            [302, 403],
            logout=True,
            debug_info="test_01_login"
        )

    @log_info
    def test_02_provider_login(self):
        """Test auth using ``SECRET_KEY`` defined in ``PROVIDERS``."""
        secret_key = ska_settings.PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']

        # Authenticate for the first time. There shall be 2 emails
        # for `create` and `info` callbacks.
        self.__test_login(
            secret_key,
            [302, 403],
            self.PROVIDER_NAME,
            logout=True,
            test_email_data={
                'emails': {
                    0: 'Welcome validate::admins!',
                    1: 'Welcome create::admins!',
                    2: 'Welcome info::admins!',
                }
            },
            debug_info="test_02_provider_login::first time"
        )

        # Sleep for just one second between first and the second tests.
        time.sleep(1)

        # Authenticate for the second time. There shall be still 2 emails
        # from the first time login (since we're in the same test method
        # still) and 2 new ones for `get` and `info` callbacks.
        self.__test_login(
            secret_key,
            [302, 403],
            self.PROVIDER_NAME,
            logout=True,
            test_email_data={
                'emails': {
                    # First round
                    0: 'Welcome validate::admins!',
                    1: 'Welcome create::admins!',
                    2: 'Welcome info::admins!',
                    # Second round
                    # TODO: this is weird. validate::admin shall not
                    # appear here twice.
                    3: 'Welcome validate::admins!',
                    4: 'Welcome validate::admins!',
                    5: 'Welcome get::admins!',
                    6: 'Welcome info::admins!',
                }
            },
            do_signature_check=False,
            debug_info="test_02_provider_login::second time"
        )

    @log_info
    def test_03_login_fail_wrong_secret_key(self):
        """Fail test auth using general ``SECRET_KEY``.

        Fail test auth using general ``SECRET_KEY`` providing wrong
        secret key.
        """
        return self.__test_login(
            ska_settings.SECRET_KEY + 'wrong',
            [403, 403],
            logout=True,
            debug_info="test_03_login_fail_wrong_secret_key"
        )

    @log_info
    def test_04_provider_login_fail_wrong_secret_key(self):
        """Fail test authentication.

        Fail test authentication using ``SECRET_KEY`` defined in `
        `PROVIDERS``, providing wrong secret key.
        """
        secret_key = ska_settings.PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        return self.__test_login(
            secret_key + 'wrong',
            [403, 403],
            self.PROVIDER_NAME,
            logout=True
        )

    @log_info
    def test_05_provider_login_fail_wrong_provider(self):
        """Test provider login fail wrong provider.

        Fail test authentication using ``SECRET_KEY`` defined in
        ``PROVIDERS``, providing wrong provider name.
        """
        secret_key = ska_settings.PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        return self.__test_login(
            secret_key + 'wrong',
            [403, 403],
            self.PROVIDER_NAME + 'wrong',
            logout=True,
            debug_info="test_05_provider_login_fail_wrong_provider"
        )

    @log_info
    @override_settings(**OVERRIDE_SETTINGS_DB_STORE_SIGNATURES_KWARGS)
    @mock.patch(
        'ska.contrib.django.ska.settings.DB_STORE_SIGNATURES',
        True
    )
    @mock.patch(
        'ska.contrib.django.ska.settings.DB_PERFORM_SIGNATURE_CHECK',
        True
    )
    def test_06_purge_stored_signatures_data(self):
        """Test purge stored signature data."""
        secret_key = ska_settings.PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        # Login
        self.__test_login(
            secret_key,
            [302, 403],
            self.PROVIDER_NAME,
            logout=True,
            debug_info="test_06_purge_stored_signatures_data"
        )

        # Duplicate signatures
        signature = Signature.objects.first()
        signature.id = None
        signature.signature += '0'
        signature.save()
        signature.id = None
        signature.signature += '0'
        signature.save()
        # There should be 3
        self.assertEqual(Signature.objects.all().count(), 3)

        # Manually set valid_until to no longer valid so that we can
        # test
        invalid_until = (
            datetime.datetime.now() - datetime.timedelta(minutes=20)
        )
        Signature.objects.update(
            valid_until=invalid_until
        )

        # Call purge command
        call_command('ska_purge_stored_signature_data')
        # All old records shall be gone
        self.assertEqual(Signature.objects.all().count(), 0)

    @log_info
    def test_07_provider_login_forbidden_email(self):
        """Test auth using ``SECRET_KEY`` defined in ``PROVIDERS``."""
        secret_key = ska_settings.PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']

        # Authenticate for the first time. There shall be 2 emails
        # for `create` and `info` callbacks.
        self.__test_login(
            secret_key,
            [403, 403],
            self.PROVIDER_NAME,
            logout=True,
            test_email_data={
                'emails': {}
            },
            auth_user_email='forbidden@example.com',
            debug_info="test_07_provider_login_forbidden_email"
        )

    @log_info
    def test_08_provider_login_forbidden_username(self):
        """Test auth using ``SECRET_KEY`` defined in ``PROVIDERS``."""
        secret_key = ska_settings.PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']

        # Authenticate for the first time. There shall be 2 emails
        # for `create` and `info` callbacks.
        self.__test_login(
            secret_key,
            [403, 403],
            self.PROVIDER_NAME,
            logout=True,
            test_email_data={
                'emails': {}
            },
            auth_user='forbidden_username',
            debug_info="test_08_provider_login_forbidden_username"
        )


if __name__ == "__main__":
    # Tests
    unittest.main()
