from __future__ import absolute_import, print_function

import datetime
import logging
import os
import random
import time
import unittest

import pytest

__title__ = 'ska.contrib.django.ska.tests.test_django_ska'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2018 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

logger = logging.getLogger(__name__)


def project_dir(base):
    """Project dir."""
    return os.path.join(os.path.dirname(__file__), base).replace('\\', '/')


PROJECT_DIR = project_dir

LOG_INFO = True


def log_info(func):
    """Logs some useful info."""
    if not LOG_INFO:
        return func

    def inner(self, *args, **kwargs):
        """Inner."""
        result = func(self, *args, **kwargs)

        logger.debug('\n\n%s', func.__name__)
        logger.debug('============================')
        if func.__doc__:
            logger.debug('""" %s """', func.__doc__.strip())
        logger.debug('----------------------------')
        if result is not None:
            logger.debug(result)
        logger.debug('\n++++++++++++++++++++++++++++')

        return result
    return inner


def change_date():
    """Change date."""
    return bool(random.randint(0, 1))


NUM_ITEMS = 5


# *********************************************************************
# *********************************************************************
# *********************************************************************

# Skipping from non-Django tests.
if os.environ.get("DJANGO_SETTINGS_MODULE", None):

    from django.core import mail
    from django.core.management import call_command
    from django.test import Client, TransactionTestCase

    from ska import sign_url
    from ska.defaults import DEFAULT_PROVIDER_PARAM
    from ska.contrib.django.ska.settings import (
        SECRET_KEY,
        DB_STORE_SIGNATURES,
        DB_PERFORM_SIGNATURE_CHECK,
        PROVIDERS
    )
    from ska.contrib.django.ska.models import Signature

    import factories

    SKA_TEST_USER_USERNAME = factories.TEST_ADMIN_USERNAME
    SKA_TEST_USER_PASSWORD = factories.TEST_PASSWORD

# *********************************************************************
# *********************************************************************
# *********************************************************************

    @pytest.mark.django_db
    def create_admin_user():
        """Create a user for testing the dashboard.

        TODO: At the moment an admin account is being tested. Automated tests
        with diverse accounts are to be implemented.
        """
        user = factories.TestAdminUsernameSuperAdminUserFactory(
            email='admin@dev.django-ska.com'
        )

    @pytest.mark.django_db
    def generate_data(num_items=NUM_ITEMS):
        """Generate data."""
        return factories.FooItemFactory.create_batch(num_items)

    # *********************************************************************
    # *********************************************************************
    # *********************************************************************

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
            if DB_STORE_SIGNATURES \
                    and DB_PERFORM_SIGNATURE_CHECK \
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
                SECRET_KEY,
                [302, 403],
                logout=True,
                debug_info="test_01_login"
            )

        @log_info
        def test_02_provider_login(self):
            """Test auth using ``SECRET_KEY`` defined in ``PROVIDERS``."""
            secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']

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
                        1: 'Welcome info::admins!',
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
                        1: 'Welcome info::admins!',
                        2: 'Welcome get::admins!',
                        3: 'Welcome info::admins!',
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
                SECRET_KEY + 'wrong',
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
            secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
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
            secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
            return self.__test_login(
                secret_key + 'wrong',
                [403, 403],
                self.PROVIDER_NAME + 'wrong',
                logout=True,
                debug_info="test_05_provider_login_fail_wrong_provider"
            )

        @log_info
        def test_06_purge_stored_signatures_data(self):
            """Test purge stored signature data."""
            secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
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
