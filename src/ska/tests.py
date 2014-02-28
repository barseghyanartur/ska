from __future__ import print_function

__title__ = 'ska.tests'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

import unittest
import datetime
from copy import copy

from six import PY3, text_type

try:
    from six.moves.urllib.parse import urlparse, parse_qs
except ImportError as e:
    if PY3:
        from urllib.parse import urlparse, parse_qs
    else:
        from urlparse import urlparse, parse_qs

from ska import Signature, RequestHelper, TIMESTAMP_FORMAT
from ska import sign_url, validate_signed_request_data, signature_to_dict
from ska import error_codes

PRINT_INFO = True
TRACK_TIME = False

def print_info(func):
    """
    Prints some useful info.
    """
    if not PRINT_INFO:
        return func

    def inner(self, *args, **kwargs):
        if TRACK_TIME:
            import simple_timer
            timer = simple_timer.Timer() # Start timer

        result = func(self, *args, **kwargs)

        if TRACK_TIME:
            timer.stop() # Stop timer

        print('\n\n%s' % func.__name__)
        print('============================')
        if func.__doc__:
            print('""" %s """' % func.__doc__.strip())
        print('----------------------------')
        if result is not None:
            print(result)
        if TRACK_TIME:
            print('done in %s seconds' % timer.duration)
        print('\n++++++++++++++++++++++++++++')

        return result
    return inner

def timestap_to_human_readable(timestamp):
    """
    Converts Unix timestamp to human readable string.

    :param float:
    :return str:
    """
    dt = datetime.datetime.fromtimestamp(float(timestamp))
    return dt.strftime(TIMESTAMP_FORMAT)

class SignatureTest(unittest.TestCase):
    """
    Tests of ``ska.Signature`` class.
    """
    def setUp(self):
        self.auth_user = 'user'
        self.secret_key = 'secret'

    @print_info
    def test_01_signature_test(self):
        """
        Signature test.
        """
        flow = []

        # Generate signature
        sig = Signature.generate_signature(
            auth_user = self.auth_user,
            secret_key = self.secret_key
            )

        flow.append(('Valid until used', sig.valid_until))
        flow.append(('Valid until (human readable)', timestap_to_human_readable(sig.valid_until)))
        flow.append(('Signature generated', sig.signature))
        flow.append(('Signature is expired', sig.is_expired()))

        # Check if not expired
        self.assertTrue(not sig.is_expired())

        # Check if valid
        validation_result = Signature.validate_signature(
                signature = sig.signature,
                auth_user = self.auth_user,
                secret_key = self.secret_key,
                valid_until = sig.valid_until,
                return_object = True
                )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    @print_info
    def test_02_signature_test_with_positive_timelap(self):
        """
        Signature test with positive timelap, when signature is made on a host
        that has a positive (greater) time difference with server. In this
        particular example, the host time is 5 minutes ahead the server time.
        """
        flow = []

        datetime_timelap = Signature.datetime_to_unix_timestamp(
            datetime.datetime.now() + datetime.timedelta(seconds=300)
            )

        flow.append(('Valid until used', datetime_timelap))
        flow.append(('Valid until used (human readable)', timestap_to_human_readable(datetime_timelap)))

        # Generate signature
        sig = Signature.generate_signature(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            valid_until = datetime_timelap
            )

        flow.append(('Signature generated', sig.signature))
        flow.append(('Signature is expired', sig.is_expired()))

        # Check if not expired
        self.assertTrue(not sig.is_expired())

        # Check if valid
        validation_result = Signature.validate_signature(
                signature = sig.signature,
                auth_user = self.auth_user,
                secret_key = self.secret_key,
                valid_until = sig.valid_until,
                return_object = True
                )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    @print_info
    def test_03_signature_test_with_negative_timelap(self):
        """
        Fail test. Signature test with negative timelap, when signature is made on
        a host that has a negative (less) time difference with server. In this
        particular example, the host time is 5 minutes behind the server time,
        which exceeds the signature lifetime.
        """
        flow = []

        datetime_timelap = Signature.datetime_to_unix_timestamp(
            datetime.datetime.now() - datetime.timedelta(seconds=300)
            )

        flow.append(('Valid until used', datetime_timelap))
        flow.append(('Valid until used (human readable)', timestap_to_human_readable(datetime_timelap)))

        # Generate signature
        sig = Signature.generate_signature(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            valid_until = datetime_timelap
            )

        flow.append(('Signature generated', sig.signature))
        flow.append(('Signature is expired', sig.is_expired()))

        # Check if not expired
        self.assertTrue(sig.is_expired())

        # Check if valid
        validation_result = Signature.validate_signature(
                signature = sig.signature,
                auth_user = self.auth_user,
                secret_key = self.secret_key,
                valid_until = sig.valid_until,
                return_object = True
                )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    @print_info
    def test_04_fail_signature_test(self):
        """
        Fail signature tests.
        """
        flow = []

        validation_result = Signature.validate_signature(
            signature = 'EBS6ipiqRLa6TY5vxIvZU30FpnM=',
            auth_user = 'fakeuser',
            secret_key = 'fakesecret',
            valid_until = 1377997396.0,
            return_object = True
            )

        flow.append(('Valid until used', 1377997396.0))
        flow.append(('Valid until used (human readable)', timestap_to_human_readable(1377997396.0)))
        flow.append(('Signature generated', 'EBS6ipiqRLa6TY5vxIvZU30FpnM='))
        flow.append(('Signature is expired', True))

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    @print_info
    def test_05_fail_signature_test_related_to_changes_in_validation_result_class(self):
        """
        Fail signature tests related to tiny changes in the `ValidationResult` class.
        """
        flow = []

        validation_result = Signature.validate_signature(
            signature = 'EBS6ipiqRLa6TY5vxIvZU30FpnM=',
            auth_user = 'fakeuser',
            secret_key = 'fakesecret',
            valid_until = 1377997396.0,
            return_object = True
            )

        if PY3:
            self.assertTrue(isinstance(validation_result.reason, map))
        else:
            self.assertTrue(isinstance(validation_result.reason, list))
        self.assertTrue(isinstance(validation_result.errors, list))
        self.assertTrue(isinstance(validation_result.message, text_type))
        self.assertTrue(isinstance(' '.join(validation_result.reason), text_type))
        self.assertTrue(isinstance(' '.join(map(text_type, validation_result.errors)), text_type))

        flow.append(validation_result.message)

        self.assertTrue(error_codes.INVALID_SIGNATURE in validation_result.errors)
        self.assertTrue(error_codes.SIGNATURE_TIMESTAMP_EXPIRED in validation_result.errors)

        return flow


def parse_url_params(url):
    """
    Parses URL params.

    :param str url:
    :return dict:
    """
    data = parse_qs(urlparse(url).query)
    for k, v in data.items():
        data[k] = v[0]


    return data

class URLHelperTest(unittest.TestCase):
    """
    Tests of ``ska.URLHelper`` class.
    """
    def setUp(self):
        self.auth_user = 'user'
        self.secret_key = 'secret'

    @print_info
    def test_01_signature_to_url(self):
        """
        Signature test.
        """
        flow = []

        # Generate signature
        signature = Signature.generate_signature(
            auth_user = self.auth_user,
            secret_key = self.secret_key
            )

        request_helper = RequestHelper(
            signature_param = 'signature',
            auth_user_param = 'auth_user',
            valid_until_param = 'valid_until'
            )

        signed_endpoint_url = request_helper.signature_to_url(
            signature = signature,
            endpoint_url = 'http://dev.example.com/api/'
            )

        flow.append(('URL generated', signed_endpoint_url))

        # Now parsing back the URL params.
        request_data = parse_url_params(signed_endpoint_url)

        validation_result = request_helper.validate_request_data(data=request_data, secret_key=self.secret_key)

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    @print_info
    def test_02_signature_to_url_fail(self):
        """
        Signature test. Fail test.
        """
        flow = []

        datetime_timelap = Signature.datetime_to_unix_timestamp(
            datetime.datetime.now() - datetime.timedelta(seconds=300)
            )

        # Generate signature
        signature = Signature.generate_signature(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            valid_until = datetime_timelap
            )

        request_helper = RequestHelper(
            signature_param = 'signature',
            auth_user_param = 'auth_user',
            valid_until_param = 'valid_until'
            )

        signed_endpoint_url = request_helper.signature_to_url(
            signature = signature,
            endpoint_url = 'http://dev.example.com/api/'
            )

        flow.append(('URL generated', signed_endpoint_url))

        # Now parsing back the URL params.
        request_data = parse_url_params(signed_endpoint_url)

        validation_result = request_helper.validate_request_data(data=request_data, secret_key=self.secret_key)

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

class ShortcutsTest(unittest.TestCase):
    """
    Tests for ``sign_url``, ``signature_to_dict`` and ``validate_signed_request_data`` shortcut functions.
    """
    def setUp(self):
        self.auth_user = 'user'
        self.secret_key = 'secret'
        self.endpoint_url = 'http://e.com/api/'

    @print_info
    def test_01_sign_url_and_validate_signed_request_data(self):
        """
        Tests for ``sign_url`` and ``validate_signed_request_data`` shortcut functions.
        """
        flow = []

        signed_url = sign_url(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            url = self.endpoint_url
        )

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        validation_result = validate_signed_request_data(
            data = request_data,
            secret_key = self.secret_key
            )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    @print_info
    def test_02_sign_url_and_validate_signed_request_data_fail(self):
        """
        Fail tests for ``sign_url`` and ``validate_signed_request_data`` shortcut functions.
        """
        flow = []

        datetime_timelap = Signature.datetime_to_unix_timestamp(
            datetime.datetime.now() - datetime.timedelta(seconds=300)
            )

        flow.append(('Valid until used', datetime_timelap))
        flow.append(('Valid until used (human readable)', timestap_to_human_readable(datetime_timelap)))

        signed_url = sign_url(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            url = self.endpoint_url,
            valid_until = datetime_timelap
        )

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        validation_result = validate_signed_request_data(
            data = request_data,
            secret_key = self.secret_key
            )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    @print_info
    def test_03_signature_to_dict_and_validate_signed_request_data(self):
        """
        Tests for ``signature_to_dict`` and ``validate_signed_request_data`` shortcut functions.
        """
        flow = []

        signature_dict = signature_to_dict(
            auth_user = self.auth_user,
            secret_key = self.secret_key
        )

        flow.append(('Dictionary created', signature_dict))

        # Now validate the signature data

        validation_result = validate_signed_request_data(
            data = signature_dict,
            secret_key = self.secret_key
            )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow


class ExtraTest(unittest.TestCase):
    """
    Test for extra data.
    """
    def setUp(self):
        self.auth_user = 'user'
        self.secret_key = 'secret'
        self.endpoint_url = 'http://e.com/api/'

    def __get_signed_url(self):
        return sign_url(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            url = self.endpoint_url,
            extra = {
                'provider': 'service1.example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@mail.example.com',
            }
            )

    @print_info
    def test_01_sign_url_and_validate_signed_request_data(self):
        """
        Tests for ``sign_url`` and ``validate_signed_request_data`` shortcut functions.
        """
        flow = []

        signed_url = self.__get_signed_url()

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        #request_data['extra'] = 'provider,first_name'

        validation_result = validate_signed_request_data(
            data = request_data,
            secret_key = self.secret_key
            )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    @print_info
    def test_02_sign_url_and_validate_signed_request_data_tumper_extra_keys_remove(self):
        """
        Fail tests for ``sign_url`` and ``validate_signed_request_data`` shortcut functions,
        as well as providing the additional data ``extra`` and data tumpering ``extra``
        keys (remove).
        """
        flow = []

        signed_url = self.__get_signed_url()

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        # ***************************************************************************
        # ****************************** Tumpering **********************************
        # ***************************************************************************
        tumpered_request_data = copy(request_data)

        tumpered_request_data['extra'] = 'provider,first_name'

        flow.append(('Request data', request_data))
        flow.append(('Tumpered request data', tumpered_request_data))

        validation_result = validate_signed_request_data(
            data = tumpered_request_data,
            secret_key = self.secret_key
            )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    @print_info
    def test_03_sign_url_and_validate_signed_request_data_tumper_extra_keys_add(self):
        """
        Fail tests for ``sign_url`` and ``validate_signed_request_data`` shortcut functions,
        as well as providing the additional data ``extra`` and data tumpering ``extra``
        keys (add).
        """
        flow = []

        signed_url = self.__get_signed_url()

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        # ***************************************************************************
        # ****************************** Tumpering **********************************
        # ***************************************************************************
        tumpered_request_data = copy(request_data)

        tumpered_request_data['extra'] += ',age'
        tumpered_request_data['age'] = 27

        flow.append(('Request data', request_data))
        flow.append(('Tumpered request data', tumpered_request_data))

        validation_result = validate_signed_request_data(
            data = tumpered_request_data,
            secret_key = self.secret_key
            )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    @print_info
    def test_04_sign_url_and_validate_signed_request_data_tumper_extra_keys_add(self):
        """
        Tests for ``sign_url`` and ``validate_signed_request_data`` shortcut functions,
        as well as providing the additional data ``extra`` and data tumpering ``extra``
        keys (add) repeated params.
        """
        flow = []

        signed_url = "{0}&provider=cervice0.example.com".format(self.__get_signed_url())

        # ***************************************************************************
        # ****************************** Tumpering **********************************
        # ***************************************************************************

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        tampered_request_data = parse_url_params(signed_url)

        # ***************************************************************************
        # ****************************** Tumpering **********************************
        # ***************************************************************************
        even_more_tumpered_request_data = copy(tampered_request_data)
        even_more_tumpered_request_data['extra'] += ',provider'

        flow.append(('Tampered request data', tampered_request_data))
        flow.append(('Even more tampered request data', even_more_tumpered_request_data))

        validation_result = validate_signed_request_data(
            data = even_more_tumpered_request_data,
            secret_key = self.secret_key
            )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow


if __name__ == "__main__":
    # Tests
    unittest.main()
