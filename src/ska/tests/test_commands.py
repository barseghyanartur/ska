import unittest

import shlex
import subprocess

from six.moves.urllib import parse

from ..shortcuts import validate_signed_request_data

__title__ = 'ska.tests.test_commands'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'GenerateSignedUrlTest',
)


class GenerateSignedUrlTest(unittest.TestCase):
    """Tests of `generate_signed_url` module and `ska-sign-url` script."""

    def setUp(self):
        """Set up."""
        self.auth_user = 'user'
        self.secret_key = 'secret'
        self.url = 'http://example.com/'

    def test_generate_signed_url(self):
        """Test `generate_signed_url` module.

        :return:
        """
        signed_url = subprocess.check_output(
            shlex.split(
                'ska-sign-url '
                '-au {auth_user} '
                '-sk {secret_key} '
                '--url {url}'.format(
                    auth_user=self.auth_user,
                    secret_key=self.secret_key,
                    url=self.url,
                )
            )
        ).strip()
        # It's necessary to `strip` the value, since in Python 2 there might
        # be a \n added at the end of the string.

        parsed_url = parse.urlparse(str(signed_url))
        parsed_query_params = parse.parse_qs(parsed_url.query)
        data = {
            'signature': parsed_query_params.get('signature')[0],
            'auth_user': parsed_query_params.get('auth_user')[0],
            'valid_until': parsed_query_params.get('valid_until')[0],
        }

        validation_result = validate_signed_request_data(data, self.secret_key)

        self.assertTrue(validation_result.result)
