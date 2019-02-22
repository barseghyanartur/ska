import unittest

from bs4 import BeautifulSoup

from django.test import Client, TransactionTestCase, override_settings

from nine import versions

from .helpers import log_info

import factories

if versions.DJANGO_GTE_1_10:
    from django.urls import reverse
else:
    from django.core.urlresolvers import reverse

__title__ = 'ska.contrib.django.ska.tests.test_templatetags'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'SkaTagsTest',
    'SkaConstanceTagsTest',
)


OVERRIDE_SETTINGS_KWARGS = {
    'AUTHENTICATION_BACKENDS': (
        'ska.contrib.django.ska.backends.constance_backend.'
        'SkaAuthenticationConstanceBackend',
        'django.contrib.auth.backends.ModelBackend',
    ),
    'ROOT_URLCONF': 'constance_urls',
}


class BaseSkaTagsTest(TransactionTestCase):
    """Base template tags tests."""

    @classmethod
    def setUpClass(cls):
        cls.templatetags_url = reverse('foo.templatetags')

    def setUp(self):
        """Set up."""
        factories.SkaSecretKeyConstanceFactory()
        factories.SkaProvidersConstanceFactory()

    def _test_sign_url(self, sign_in_link_class):
        """Test `sign_url` or `provider_sign_url` template tag."""
        client = Client()

        response_1 = client.get(self.templatetags_url)
        soup_1 = BeautifulSoup(
            getattr(response_1, 'content', ''),
            features="html.parser"
        )

        sign_in_link_element_1 = soup_1.find(
            'a',
            attrs={'class': sign_in_link_class}
        )
        sign_in_url = sign_in_link_element_1.attrs.get('href')
        sign_in_element_classes_1 = sign_in_link_element_1.attrs.get('class')
        self.assertIn('logged-out', sign_in_element_classes_1)
        self.assertNotIn('logged-in', sign_in_element_classes_1)

        response_2 = client.get(sign_in_url, follow=True)
        soup_2 = BeautifulSoup(
            getattr(response_2, 'content', ''),
            features="html.parser"
        )
        sign_in_link_element_2 = soup_2.find(
            'a',
            attrs={'class': sign_in_link_class}
        )
        sign_in_element_classes_2 = sign_in_link_element_2.attrs.get('class')
        self.assertNotIn('logged-out', sign_in_element_classes_2)
        self.assertIn('logged-in', sign_in_element_classes_2)


class SkaTagsTest(BaseSkaTagsTest):
    """Testing `ska_tags` functionality."""

    @log_info
    def test_01_sign_url(self):
        """Test `sign_url` template tag."""
        return self._test_sign_url(
            sign_in_link_class='signed-url'
        )

    @log_info
    def test_02_provider_sign_url(self):
        """Test `provider_sign_url` template tag."""
        return self._test_sign_url(
            sign_in_link_class='provider-signed-url'
        )


class SkaConstanceTagsTest(BaseSkaTagsTest):
    """Testing `ska_constance_tags` functionality."""

    @log_info
    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_01_sign_url(self):
        """Test `sign_url` template tag."""
        return self._test_sign_url(
            sign_in_link_class='signed-url'
        )

    @log_info
    @override_settings(**OVERRIDE_SETTINGS_KWARGS)
    def test_02_provider_sign_url(self):
        """Test `provider_sign_url` template tag."""
        return self._test_sign_url(
            sign_in_link_class='provider-signed-url'
        )


if __name__ == '__main__':
    unittest.main()
