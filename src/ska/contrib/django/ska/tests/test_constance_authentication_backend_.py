from __future__ import absolute_import, print_function

import datetime
import logging
import time
import unittest

from constance import config
from constance.test import override_config

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

__title__ = 'ska.contrib.django.ska.tests.test_constance_authentication_backend'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'SkaAuthenticationConstanceBackendTest',
)

logger = logging.getLogger(__name__)


# *********************************************************************
# *********************************************************************
# *********************************************************************

SKA_TEST_USER_USERNAME = factories.TEST_ADMIN_USERNAME
SKA_TEST_USER_PASSWORD = factories.TEST_PASSWORD

OVERRIDE_CONSTANCE_KWARGS = {
    # 'SKA_PROVIDERS': {
    #     # Client 1, group users
    #     'client_1.users': {
    #         'SECRET_KEY': 'client-1-users-secret-key',
    #     },
    #
    #     # Client 1, group power_users
    #     'client_1.power_users': {
    #         'SECRET_KEY': 'client-1-power-users-secret-key',
    #         'USER_CREATE_CALLBACK': 'foo.ska_callbacks.'
    #                                 'client1_power_users_create',
    #     },
    #
    #     # Client 1, group admins
    #     'client_1.admins': {
    #         'SECRET_KEY': 'client-1-admins-secret-key',
    #         'USER_CREATE_CALLBACK': 'foo.ska_callbacks.'
    #                                 'client1_admins_create',
    #         'USER_GET_CALLBACK': 'foo.ska_callbacks.'
    #                              'client1_admins_get',
    #         'USER_INFO_CALLBACK': 'foo.ska_callbacks.'
    #                               'client1_admins_info_constance',
    #         'REDIRECT_AFTER_LOGIN': '/admin/'
    #     },
    # }
}
OVERRIDE_SETTINGS_KWARGS = {
    'AUTHENTICATION_BACKENDS': (
        'ska.contrib.django.ska.backends.constance_backend.'
        'SkaAuthenticationConstanceBackend',
        'django.contrib.auth.backends.ModelBackend',
    ),
    'ROOT_URLCONF': 'constance_urls',
}

OVERRIDE_SETTINGS_DB_STORE_SIGNATURES_KWARGS = {
    'SKA_DB_STORE_SIGNATURES': True,
    'SKA_DB_PERFORM_SIGNATURE_CHECK': True,
}


@pytest.mark.django_db
class SkaAuthenticationConstanceBackendTest(TransactionTestCase):
    """Tests for auth constance backend."""

    pytestmark = pytest.mark.django_db

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def setUp(self):
        self.AUTH_USER = 'test_auth_backend_user'
        self.AUTH_USER_EMAIL = 'test_ska_auth_user@mail.example.com'
        self.AUTH_USER_FIRST_NAME = 'John'
        self.AUTH_USER_LAST_NAME = 'Doe'
        self.PROVIDER_NAME = 'client_1.admins'
        self.LOGIN_URL = '/ska/login/'

        factories.SkaProvidersConstanceFactory()

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    @override_config(**OVERRIDE_CONSTANCE_KWARGS)
    def __test_login(self,
                     secret_key,
                     response_codes,
                     provider_name=None,
                     logout=False,
                     test_email_data=None,
                     do_signature_check=True,
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
        :return:
        """
        flow = []

        first_response_code, second_response_code = response_codes

        # Testing signed URLs
        extra = {
            'email': self.AUTH_USER_EMAIL,
            'first_name': self.AUTH_USER_FIRST_NAME,
            'last_name': self.AUTH_USER_LAST_NAME,
        }
        if provider_name:
            extra.update({DEFAULT_PROVIDER_PARAM: provider_name})

        signed_login_url = sign_url(
            auth_user=self.AUTH_USER,
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

    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    @override_config(**OVERRIDE_CONSTANCE_KWARGS)
    def __logout(self):
        """Log out."""
        self._client.logout()

    @log_info
    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    @override_config(**OVERRIDE_CONSTANCE_KWARGS)
    def test_01_login(self):
        """Test auth using general ``SECRET_KEY``."""
        return self.__test_login(
            ska_settings.SECRET_KEY,
            [302, 403],
            logout=True,
            debug_info="test_01_login"
        )

    @log_info
    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    @override_config(**OVERRIDE_CONSTANCE_KWARGS)
    def test_02_provider_login(self):
        """Test auth using ``SECRET_KEY`` defined in ``PROVIDERS``."""
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']

        # Authenticate for the first time. There shall be 2 emails
        # for `create` and `info` callbacks.
        self.__test_login(
            secret_key,
            [302, 403],
            self.PROVIDER_NAME,
            logout=True,
            test_email_data={
                'emails': {
                    0: 'Welcome create::admins!',
                    1: 'Welcome info::constance::admins!',
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
                    0: 'Welcome create::admins!',
                    1: 'Welcome info::constance::admins!',
                    2: 'Welcome get::admins!',
                    3: 'Welcome info::constance::admins!',
                }
            },
            do_signature_check=False,
            debug_info="test_02_provider_login::second time"
        )

    @log_info
    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    @override_config(**OVERRIDE_CONSTANCE_KWARGS)
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
    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    @override_config(**OVERRIDE_CONSTANCE_KWARGS)
    def test_04_provider_login_fail_wrong_secret_key(self):
        """Fail test authentication.

        Fail test authentication using ``SECRET_KEY`` defined in `
        `PROVIDERS``, providing wrong secret key.
        """
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        return self.__test_login(
            secret_key + 'wrong',
            [403, 403],
            self.PROVIDER_NAME,
            logout=True
        )

    @log_info
    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    @override_config(**OVERRIDE_CONSTANCE_KWARGS)
    def test_05_provider_login_fail_wrong_provider(self):
        """Test provider login fail wrong provider.

        Fail test authentication using ``SECRET_KEY`` defined in
        ``PROVIDERS``, providing wrong provider name.
        """
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
        return self.__test_login(
            secret_key + 'wrong',
            [403, 403],
            self.PROVIDER_NAME + 'wrong',
            logout=True,
            debug_info="test_05_provider_login_fail_wrong_provider"
        )

    @log_info
    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    @override_settings(**OVERRIDE_SETTINGS_DB_STORE_SIGNATURES_KWARGS)
    @override_config(**OVERRIDE_CONSTANCE_KWARGS)
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
        secret_key = config.SKA_PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
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


if __name__ == "__main__":
    # Tests
    unittest.main()
