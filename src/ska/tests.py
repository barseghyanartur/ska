__title__ = 'ska.tests'
__version__ = '0.2'
__build__ = 0x000002
__author__ = 'Artur Barseghyan'

import unittest
import datetime
import time
from urlparse import urlparse, parse_qs

from ska import Signature, RequestHelper, TIMESTAMP_FORMAT, sign_url, validate_signed_request_data

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

        print '\n\n%s' % func.__name__
        print '============================'
        if func.__doc__:
            print '""" %s """' % func.__doc__.strip()
        print '----------------------------'
        if result is not None: print result
        if TRACK_TIME:
            print 'done in %s seconds' % timer.duration
        print '\n++++++++++++++++++++++++++++'

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
        workflow = []

        # Generate signature
        sig = Signature.generate_signature(
            auth_user = self.auth_user,
            secret_key = self.secret_key
            )

        workflow.append(('Valid until used', sig.valid_until))
        workflow.append(('Valid until (human readable)', timestap_to_human_readable(sig.valid_until)))
        workflow.append(('Signature generated', sig.signature))
        workflow.append(('Signature is expired', sig.is_expired()))

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

        workflow.append(('Signature is valid', validation_result.result))
        workflow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return workflow

    @print_info
    def test_02_signature_test_with_positive_timelap(self):
        """
        Signature test with positive timelap, when signature is made on a host
        that has a positive (greater) time difference with server. In this
        particular example, the host time is 5 minutes ahead the server time.
        """
        workflow = []
        
        datetime_timelap = Signature.datetime_to_unix_timestamp(
            datetime.datetime.now() + datetime.timedelta(seconds=300)
            )

        workflow.append(('Valid until used', datetime_timelap))
        workflow.append(('Valid until used (human readable)', timestap_to_human_readable(datetime_timelap)))

        # Generate signature
        sig = Signature.generate_signature(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            valid_until = datetime_timelap
            )

        workflow.append(('Signature generated', sig.signature))
        workflow.append(('Signature is expired', sig.is_expired()))

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

        workflow.append(('Signature is valid', validation_result.result))
        workflow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return workflow

    @print_info
    def test_03_signature_test_with_negative_timelap(self):
        """
        Fail test. Signature test with negative timelap, when signature is made on
        a host that has a negative (less) time difference with server. In this
        particular example, the host time is 5 minutes behind the server time,
        which exceeds the signature lifetime.
        """
        workflow = []

        datetime_timelap = Signature.datetime_to_unix_timestamp(
            datetime.datetime.now() - datetime.timedelta(seconds=300)
            )

        workflow.append(('Valid until used', datetime_timelap))
        workflow.append(('Valid until used (human readable)', timestap_to_human_readable(datetime_timelap)))

        # Generate signature
        sig = Signature.generate_signature(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            valid_until = datetime_timelap
            )

        workflow.append(('Signature generated', sig.signature))
        workflow.append(('Signature is expired', sig.is_expired()))

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

        workflow.append(('Signature is valid', validation_result.result))
        workflow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return workflow

    @print_info
    def test_04_fail_signature_test(self):
        """
        Fail signature tests.
        """
        workflow = []

        validation_result = Signature.validate_signature(
            signature = 'EBS6ipiqRLa6TY5vxIvZU30FpnM=',
            auth_user = 'fakeuser',
            secret_key = 'fakesecret',
            valid_until = 1377997396.0,
            return_object = True
            )

        workflow.append(('Valid until used', 1377997396.0))
        workflow.append(('Valid until used (human readable)', timestap_to_human_readable(1377997396.0)))
        workflow.append(('Signature generated', 'EBS6ipiqRLa6TY5vxIvZU30FpnM='))
        workflow.append(('Signature is expired', True))

        workflow.append(('Signature is valid', validation_result.result))
        workflow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return workflow

def parse_url_params(url):
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
        workflow = []

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

        workflow.append(('URL generated', signed_endpoint_url))

        # Now parsing back the URL params.
        request_data = parse_url_params(signed_endpoint_url)

        validation_result = request_helper.validate_request_data(data=request_data, secret_key=self.secret_key)

        workflow.append(('Signature is valid', validation_result.result))
        workflow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return workflow

    @print_info
    def test_02_signature_to_url_fail(self):
        """
        Signature test. Fail test.
        """
        workflow = []

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

        workflow.append(('URL generated', signed_endpoint_url))

        # Now parsing back the URL params.
        request_data = parse_url_params(signed_endpoint_url)

        validation_result = request_helper.validate_request_data(data=request_data, secret_key=self.secret_key)

        workflow.append(('Signature is valid', validation_result.result))
        workflow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return workflow

class ShortcutsTest(unittest.TestCase):
    """
    Tests for ``sign_url`` and ``validate_signed_request_data`` shortcut functions.
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
        workflow = []

        signed_url = sign_url(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            url = self.endpoint_url
        )

        workflow.append(('URL generated', signed_url))

        # Now parsing back the URL params and test the 
        request_data = parse_url_params(signed_url)

        validation_result = validate_signed_request_data(
            data = request_data,
            secret_key = self.secret_key
            )

        workflow.append(('Signature is valid', validation_result.result))
        workflow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return workflow

    @print_info
    def test_02_sign_url_and_validate_signed_request_data_fail(self):
        """
        Fail tests for ``sign_url`` and ``validate_signed_request_data`` shortcut functions.
        """
        workflow = []

        datetime_timelap = Signature.datetime_to_unix_timestamp(
            datetime.datetime.now() - datetime.timedelta(seconds=300)
            )

        workflow.append(('Valid until used', datetime_timelap))
        workflow.append(('Valid until used (human readable)', timestap_to_human_readable(datetime_timelap)))

        signed_url = sign_url(
            auth_user = self.auth_user,
            secret_key = self.secret_key,
            url = self.endpoint_url,
            valid_until = datetime_timelap
        )

        workflow.append(('URL generated', signed_url))

        # Now parsing back the URL params and test the
        request_data = parse_url_params(signed_url)

        validation_result = validate_signed_request_data(
            data = request_data,
            secret_key = self.secret_key
            )

        workflow.append(('Signature is valid', validation_result.result))
        workflow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return workflow


if __name__ == "__main__":
    # Tests
    unittest.main()
