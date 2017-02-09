from __future__ import absolute_import, print_function

import os
import logging
import random
import unittest

import pytest

import radar

from six import PY3
from six.moves import range as xrange

# from ska.gettext import _

if not PY3:
    from string import translate, maketrans, punctuation
else:
    from string import punctuation

__title__ = 'ska.contrib.django.ska.tests.test_django_ska'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

logger = logging.getLogger(__name__)


def project_dir(base):
    """Project dir."""
    return os.path.join(os.path.dirname(__file__), base).replace('\\', '/')


PROJECT_DIR = project_dir

SKA_TEST_USER_USERNAME = 'test_admin'
SKA_TEST_USER_PASSWORD = 'test'
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


# *********************************************************************
# *********************************************************************
# *********************************************************************

FACTORY = """
    Sed dictum in tellus non iaculis. Aenean ac interdum ipsum. Etiam tempor
    quis ante vel rhoncus. Nulla facilisi. Curabitur iaculis consequat odio
    ut imperdiet? Integer accumsan; nisl vitae fermentum malesuada, sapien
    nulla sodales orci, et elementum lacus purus vel purus! Nullam orci neque,
    tristique in porta id, pretium ac sem. Fusce non est risus. Fusce
    convallis tellus augue, quis volutpat tellus dapibus sagittis. Integer
    lacinia commodo risus vel cursus. Etiam vitae dui in dolor porta luctus
    sed id elit. Nulla et est nec magna facilisis sagittis. Praesent tincidunt
    dictum lectus, sed aliquam eros. Donec placerat tortor ut lorem facilisis
    congue. Quisque ac risus nibh. Etiam ultrices nibh justo; sed mollis
    ipsum dapibus vitae. Ut vitae molestie erat. Mauris ac justo quis ante
    posuere vehicula. Vivamus accumsan mi volutpat diam lacinia, vitae semper
    lectus pharetra. Cras ultrices arcu nec viverra consectetur. Cras placerat
    ante quis dui consequat cursus. Nulla at enim dictum, consectetur ligula
    eget, vehicula nisi. Suspendisse eu ligula vitae est tristique accumsan
    nec adipiscing risus. Donec tempus dui eget mollis fringilla. Fusce
    eleifend lacus lectus, vel ornare felis lacinia ut. Morbi vel adipiscing
    augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices
    posuere cubilia Curae; Cras mattis pulvinar lacus, vitae pulvinar magna
    egestas non. Aliquam in urna quis leo feugiat faucibus. Aliquam erat
    volutpat. Maecenas non mauris libero. Suspendisse nisi lorem, cursus a
    tristique a, porttitor in nisl. Mauris pellentesque gravida mi non mattis.
    Cras mauris ligula, interdum semper tincidunt sed, ornare a ipsum. Nulla
    ultrices tempus tortor vitae vehicula.Etiam at augue suscipit, vehicula
    sapien sit amet; eleifend orci. Etiam venenatis leo nec cursus mattis.
    Nulla suscipit nec lorem et lobortis. Donec interdum vehicula massa sed
    aliquam. Praesent eleifend mi sed mi pretium pellentesque. In in nisi
    tincidunt, commodo lorem quis; tincidunt nisl. In suscipit quam a
    vehicula tincidunt! Fusce vitae varius nunc. Proin at ipsum ac tellus
    hendrerit ultricies. Phasellus auctor hendrerit sapien viverra facilisis.
    Suspendisse lacus erat, cursus at dolor in, vulputate convallis sapien.
    Etiam augue nunc, lobortis vel viverra sit amet, pretium et lacus.
    Pellentesque elementum lectus eget massa tempus elementum? Nulla nec
    auctor dolor. Aliquam congue purus quis libero fermentum cursus. Etiam
    quis massa ac nisl accumsan convallis vitae ac augue. Mauris neque est,
    posuere quis dolor non, volutpat gravida tortor. Cum sociis natoque
    penatibus et magnis dis parturient montes, nascetur ridiculus mus.
    Vivamus ullamcorper, urna at ultrices aliquam, orci libero gravida ligula,
    non pulvinar sem magna sed tortor. Sed elementum leo viverra ipsum aliquet
    convallis. Suspendisse scelerisque auctor sapien. Mauris enim nisl,
    sollicitudin at rhoncus vitae, convallis nec mauris. Phasellus
    sollicitudin dui ut luctus consectetur. Vivamus placerat, neque id
    sagittis porttitor, nunc quam varius dolor, sit amet egestas nulla
    risus eu odio. Mauris gravida eleifend laoreet. Aenean a nulla nisl.
    Integer pharetra magna adipiscing, imperdiet augue ac, blandit felis.
    Cras id aliquam neque, vel consequat sapien.Duis eget vulputate ligula.
    Aliquam ornare dui non nunc laoreet, non viverra dolor semper.
"""

if not PY3:
    def split_words(val):
        """Split words."""
        return list(
            set(
                translate(
                    val.lower(),
                    maketrans(punctuation, ' ' * len(punctuation))
                ).split()
            )
        )
else:
    def split_words(val):
        """Split words."""
        return list(
            set(
                val.lower().translate(
                    str.maketrans("", "", punctuation)
                ).split()
            )
        )


def split_sentences(val):
    """Split sentences."""
    return val.split('?')


def change_date():
    """Change date."""
    return bool(random.randint(0, 1))


WORDS = split_words(FACTORY)
SENTENCES = split_sentences(FACTORY)
NUM_ITEMS = 5


# *********************************************************************
# *********************************************************************
# *********************************************************************

# Skipping from non-Django tests.
if os.environ.get("DJANGO_SETTINGS_MODULE", None):

    from django.test import Client, TransactionTestCase
    from django.utils.text import slugify
    from django.contrib.auth.models import User

    from ska import sign_url
    from ska.defaults import DEFAULT_PROVIDER_PARAM
    from ska.contrib.django.ska.settings import (
        SECRET_KEY,
        DB_STORE_SIGNATURES,
        DB_PERFORM_SIGNATURE_CHECK,
        PROVIDERS
    )

    from foo.models import FooItem

# *********************************************************************
# *********************************************************************
# *********************************************************************

    @pytest.mark.django_db
    def create_admin_user():
        """Create a user for testing the dashboard.

        TODO: At the moment an admin account is being tested. Automated tests
        with diverse accounts are to be implemented.
        """
        user = User()
        user.username = SKA_TEST_USER_USERNAME
        user.email = 'admin@dev.django-ska.com'
        user.is_superuser = True
        user.is_staff = True
        user.set_password(SKA_TEST_USER_PASSWORD)

        try:
            user.save()
        except Exception:
            pass

    @pytest.mark.django_db
    def generate_data(num_items=NUM_ITEMS):
        """Generate data."""
        words = WORDS[:]

        random_date = radar.random_datetime()

        for index in xrange(num_items):
            # Saving an item to database
            item = FooItem()
            random_name = words[random.randint(0, len(words) - 1)]

            if not PY3:
                item.title = unicode(random_name).capitalize()
                item.body = unicode(
                    SENTENCES[random.randint(0, len(SENTENCES) - 1)]
                )
            else:
                item.title = str(random_name).capitalize()
                item.body = str(
                    SENTENCES[random.randint(0, len(SENTENCES) - 1)]
                )

            item.slug = slugify(item.title)
            random_date = radar.random_datetime() \
                if change_date() \
                else random_date
            item.date_published = random_date

            try:
                item.save()
                words.remove(random_name)

                if 0 == len(words):
                    words = WORDS

            except Exception as err:
                print(err)

    # *********************************************************************
    # *********************************************************************
    # *********************************************************************

    @pytest.mark.django_db
    class SkaDecoratorsTest(TransactionTestCase):
        """Testing model- and view- decorators."""

        pytestmark = pytest.mark.django_db

        def setUp(self):
            generate_data()

            # Testing the URLs
            self.item = FooItem._default_manager.all()[0]

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

        # @log_info
        # def test_04_extra(self):
        #     """Testing extra dict."""
        #     # TODO

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

        def __test_login(self, secret_key, response_codes, provider_name=None):
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
            client = Client()
            response = client.get(signed_login_url, {})
            response_status_code = getattr(response, 'status_code', None)
            # if response.status_code not in (first_response_code,):
            #     pytest.set_trace()
            self.assertIn(response_status_code, (first_response_code,))
            flow.append(
                ('Response status code for signed URL', response_status_code)
            )

            if DB_STORE_SIGNATURES and DB_PERFORM_SIGNATURE_CHECK:
                # Testing again with signed URL and this time, it should fail
                client = Client()
                response = client.get(signed_login_url, {})
                response_status_code = getattr(response, 'status_code', None)
                self.assertIn(response_status_code, (second_response_code,))
                flow.append(
                    (
                        'Response status '
                        'code for signed URL', response_status_code
                    )
                )

            return flow

        @log_info
        def test_01_login(self):
            """Test auth using general ``SECRET_KEY``."""
            return self.__test_login(SECRET_KEY, [302, 403])

        @log_info
        def test_02_provider_login(self):
            """Test auth using ``SECRET_KEY`` defined in ``PROVIDERS``."""
            secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
            return self.__test_login(
                secret_key,
                [302, 403],
                self.PROVIDER_NAME
            )

        @log_info
        def test_03_login_fail_wrong_secret_key(self):
            """Fail test auth using general ``SECRET_KEY``.

            Fail test auth using general ``SECRET_KEY`` providing wrong
            secret key.
            """
            return self.__test_login(SECRET_KEY + 'wrong', [403, 403])

        @log_info
        def test_04_provider_login_fail_wrong_secret_key(self):
            """Fail test authentication.

            Fail test authentication using ``SECRET_KEY`` defined in `
            `PROVIDERS``, providing wrong secret key.
            """
            secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
            return self.__test_login(
                secret_key + 'wrong', [403, 403], self.PROVIDER_NAME
            )

        @log_info
        def test_05_provider_login_fail_wrong_provider(self):
            """Test provider login fail wrong provider.

            Fail test authentication using ``SECRET_KEY`` defined in
            ``PROVIDERS``, providing wrong provider name.
            """
            secret_key = PROVIDERS[self.PROVIDER_NAME]['SECRET_KEY']
            return self.__test_login(
                secret_key + 'wrong', [403, 403], self.PROVIDER_NAME + 'wrong'
            )


if __name__ == "__main__":
    # Tests
    unittest.main()
