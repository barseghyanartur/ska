import unittest
import datetime
from copy import copy

from six import PY3, text_type

from .. import (
    Signature,
    RequestHelper,
    HMACMD5Signature,
    HMACSHA1Signature,
    HMACSHA224Signature,
    HMACSHA256Signature,
    HMACSHA384Signature,
    HMACSHA512Signature,
)
from .. import sign_url, validate_signed_request_data, signature_to_dict
from .. import error_codes
from .base import log_info, timestamp_to_human_readable, parse_url_params

__title__ = 'ska.tests.test_core'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'SignatureTest',
    'URLHelperTest',
    'ShortcutsTest',
    'ExtraTest',
)


class SignatureTest(unittest.TestCase):
    """Tests of `ska.Signature` class."""

    def setUp(self):
        """Set up."""
        self.auth_user = 'user'
        self.secret_key = 'secret'
        self.signature_classes = (
            HMACMD5Signature,
            HMACSHA1Signature,
            HMACSHA224Signature,
            HMACSHA256Signature,
            HMACSHA384Signature,
            HMACSHA512Signature,
        )

    @log_info
    def __test_01_signature_test(self, signature_cls=Signature):
        """Signature test."""
        flow = []

        flow.append(('Signature class', signature_cls))

        # Generate signature
        sig = signature_cls.generate_signature(
            auth_user=self.auth_user,
            secret_key=self.secret_key
        )

        flow.append(('Valid until used', sig.valid_until))
        flow.append(('Valid until (human readable)',
                     timestamp_to_human_readable(sig.valid_until)))
        flow.append(('Signature generated', sig.signature))
        flow.append(('Signature is expired', sig.is_expired()))

        # Check if not expired
        self.assertTrue(not sig.is_expired())

        # Check if valid
        validation_result = signature_cls.validate_signature(
            signature=sig.signature,
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            valid_until=sig.valid_until,
            return_object=True
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    def test_01_signature_test(self):
        """Signature test."""
        flow = []
        for signature_cls in self.signature_classes:
            flow += self.__test_01_signature_test(signature_cls=signature_cls)
        return flow

    @log_info
    def __test_02_signature_test_with_positive_time_lapse(
            self, signature_cls=Signature):
        """Signature test with positive time-lapse.

        When signature is made on a host that has a positive (greater) time
        difference with server. In this particular example, the host time is
        5 minutes ahead the server time.
        """
        flow = []

        flow.append(('Signature class', signature_cls))

        datetime_time_lapse = signature_cls.datetime_to_unix_timestamp(
            datetime.datetime.now() + datetime.timedelta(seconds=300)
        )

        flow.append(('Valid until used', datetime_time_lapse))
        flow.append(('Valid until used (human readable)',
                     timestamp_to_human_readable(datetime_time_lapse)))

        # Generate signature
        sig = signature_cls.generate_signature(
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            valid_until=datetime_time_lapse
        )

        flow.append(('Signature generated', sig.signature))
        flow.append(('Signature is expired', sig.is_expired()))

        # Check if not expired
        self.assertTrue(not sig.is_expired())

        # Check if valid
        validation_result = signature_cls.validate_signature(
            signature=sig.signature,
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            valid_until=sig.valid_until,
            return_object=True
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    def test_02_signature_test_with_positive_time_lapse(self):
        """Signature test with positive time-lapse.

        When signature is made on a host that has a positive (greater) time
        difference with server. In this particular example, the host time is
        5 minutes ahead the server time.
        """
        flow = []
        for signature_cls in self.signature_classes:
            flow += self.__test_02_signature_test_with_positive_time_lapse(
                signature_cls=signature_cls
            )
        return flow

    @log_info
    def __test_03_signature_test_with_negative_time_lapse(
            self, signature_cls=Signature):
        """Fail test for signature test with negative time-lapse.

        When signature is made on a host that has a negative (less) time
        difference with server. In this particular example, the host time is
        5 minutes behind the server time, which exceeds the signature
        lifetime.
        """
        flow = []

        flow.append(('Signature class', signature_cls))

        datetime_time_lapse = signature_cls.datetime_to_unix_timestamp(
            datetime.datetime.now() - datetime.timedelta(seconds=300)
        )

        flow.append(('Valid until used', datetime_time_lapse))
        flow.append(('Valid until used (human readable)',
                     timestamp_to_human_readable(datetime_time_lapse)))

        # Generate signature
        sig = signature_cls.generate_signature(
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            valid_until=datetime_time_lapse
        )

        flow.append(('Signature generated', sig.signature))
        flow.append(('Signature is expired', sig.is_expired()))

        # Check if not expired
        self.assertTrue(sig.is_expired())

        # Check if valid
        validation_result = signature_cls.validate_signature(
            signature=sig.signature,
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            valid_until=sig.valid_until,
            return_object=True
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    def test_03_signature_test_with_negative_time_lapse(self):
        """Fail test. Signature test with negative time-lapse.

        When signature is made on
        a host that has a negative (less) time difference with server. In this
        particular example, the host time is 5 minutes behind the server time,
        which exceeds the signature lifetime.
        """
        flow = []
        for signature_cls in self.signature_classes:
            flow += self.__test_03_signature_test_with_negative_time_lapse(
                signature_cls=signature_cls
            )
        return flow

    @log_info
    def __test_04_fail_signature_test(self, signature_cls=Signature):
        """Fail signature tests."""
        flow = []

        flow.append(('Signature class', signature_cls))

        validation_result = signature_cls.validate_signature(
            signature='EBS6ipiqRLa6TY5vxIvZU30FpnM=',
            auth_user='fakeuser',
            secret_key='fakesecret',
            valid_until=1377997396.0,
            return_object=True
        )

        flow.append(('Valid until used', 1377997396.0))
        flow.append(('Valid until used (human readable)',
                     timestamp_to_human_readable(1377997396.0)))
        flow.append(('Signature generated', 'EBS6ipiqRLa6TY5vxIvZU30FpnM='))
        flow.append(('Signature is expired', True))

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    def test_04_fail_signature_test(self):
        """Fail signature tests."""
        flow = []
        for signature_cls in self.signature_classes:
            flow += self.__test_04_fail_signature_test(
                signature_cls=signature_cls
            )
        return flow

    @log_info
    def __test_05_fail_signature_test_validation_result_class(
            self, signature_cls=Signature):
        """Fail signature tests for `ValidationResult` class."""
        flow = []

        flow.append(('Signature class', signature_cls))

        validation_result = signature_cls.validate_signature(
            signature='EBS6ipiqRLa6TY5vxIvZU30FpnM=',
            auth_user='fakeuser',
            secret_key='fakesecret',
            valid_until=1377997396.0,
            return_object=True
        )

        if PY3:
            self.assertIsInstance(validation_result.reason, map)
        else:
            self.assertIsInstance(validation_result.reason, list)
        self.assertIsInstance(validation_result.errors, list)
        self.assertIsInstance(validation_result.message, text_type)
        self.assertIsInstance(' '.join(validation_result.reason), text_type)
        self.assertIsInstance(
            ' '.join(map(text_type, validation_result.errors)),
            text_type
        )

        flow.append(validation_result.message)

        self.assertIn(error_codes.INVALID_SIGNATURE,
                      validation_result.errors)
        self.assertIn(error_codes.SIGNATURE_TIMESTAMP_EXPIRED,
                      validation_result.errors)

        return flow

    def test_05_fail_signature_test_validation_result_class(self):
        """Fail signature tests of the `ValidationResult` class."""
        flow = []
        for signature_cls in self.signature_classes:
            flow += \
                self.__test_05_fail_signature_test_validation_result_class(
                    signature_cls=signature_cls
                )
        return flow


class URLHelperTest(unittest.TestCase):
    """Tests of `ska.URLHelper` class."""

    def setUp(self):
        """Set up."""
        self.auth_user = 'user'
        self.secret_key = 'secret'
        self.signature_classes = (
            HMACMD5Signature,
            HMACSHA1Signature,
            HMACSHA224Signature,
            HMACSHA256Signature,
            HMACSHA384Signature,
            HMACSHA512Signature,
        )

    @log_info
    def __test_01_signature_to_url(self, signature_cls=Signature):
        """Signature test."""
        flow = []

        flow.append(('Signature class', signature_cls))

        # Generate signature
        signature = signature_cls.generate_signature(
            auth_user=self.auth_user,
            secret_key=self.secret_key
        )

        request_helper = RequestHelper(
            signature_param='signature',
            auth_user_param='auth_user',
            valid_until_param='valid_until',
            signature_cls=signature_cls
        )

        signed_endpoint_url = request_helper.signature_to_url(
            signature=signature,
            endpoint_url='http://dev.example.com/api/'
        )

        flow.append(('URL generated', signed_endpoint_url))

        # Now parsing back the URL params.
        request_data = parse_url_params(signed_endpoint_url)

        validation_result = request_helper.validate_request_data(
            data=request_data,
            secret_key=self.secret_key
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    def test_01_signature_to_url(self):
        """Signature test."""
        flow = []
        for signature_cls in self.signature_classes:
            flow += self.__test_01_signature_to_url(
                signature_cls=signature_cls
            )
        return flow

    @log_info
    def __test_02_signature_to_url_fail(self, signature_cls=Signature):
        """Signature test. Fail test."""
        flow = []

        flow.append(('Signature class', signature_cls))

        datetime_time_lapse = signature_cls.datetime_to_unix_timestamp(
            datetime.datetime.now() - datetime.timedelta(seconds=300)
        )

        # Generate signature
        signature = signature_cls.generate_signature(
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            valid_until=datetime_time_lapse
        )

        request_helper = RequestHelper(
            signature_param='signature',
            auth_user_param='auth_user',
            valid_until_param='valid_until',
            signature_cls=signature_cls
        )

        signed_endpoint_url = request_helper.signature_to_url(
            signature=signature,
            endpoint_url='http://dev.example.com/api/'
        )

        flow.append(('URL generated', signed_endpoint_url))

        # Now parsing back the URL params.
        request_data = parse_url_params(signed_endpoint_url)

        validation_result = request_helper.validate_request_data(
            data=request_data,
            secret_key=self.secret_key
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    def test_02_signature_to_url_fail(self):
        """Signature test. Fail test."""
        flow = []
        for signature_cls in self.signature_classes:
            flow += self.__test_02_signature_to_url_fail(
                signature_cls=signature_cls
            )
        return flow


class ShortcutsTest(unittest.TestCase):
    """Tests for shortcut functions.

    The following shortcut functions are tested: `sign_url`,
    `signature_to_dict` and `validate_signed_request_data`.
    """

    def setUp(self):
        """Set up."""
        self.auth_user = 'user'
        self.secret_key = 'secret'
        self.endpoint_url = 'http://e.com/api/'
        self.signature_classes = (
            HMACMD5Signature,
            HMACSHA1Signature,
            HMACSHA224Signature,
            HMACSHA256Signature,
            HMACSHA384Signature,
            HMACSHA512Signature,
        )

    @log_info
    def __test_sign_url_validate_signed_request_data(
            self, signature_cls=Signature):
        """Tests for `sign_url` & `validate_signed_request_data`."""
        flow = []

        flow.append(('Signature class', signature_cls))

        signed_url = sign_url(
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            url=self.endpoint_url
        )

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        validation_result = validate_signed_request_data(
            data=request_data,
            secret_key=self.secret_key
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    def test_01_sign_url_and_validate_signed_request_data(self):
        """Tests for ``sign_url`` & ``validate_signed_request_data``."""
        flow = []
        for signature_cls in self.signature_classes:
            flow += self.__test_sign_url_validate_signed_request_data(
                signature_cls=signature_cls
            )
        return flow

    @log_info
    def __test_sign_url_validate_signed_request_data_fail(
            self, signature_cls=Signature):
        """Fail tests for `sign_url` & `validate_signed_request_data`."""
        flow = []

        flow.append(('Signature class', signature_cls))

        datetime_time_lapse = signature_cls.datetime_to_unix_timestamp(
            datetime.datetime.now() - datetime.timedelta(seconds=300)
        )

        flow.append(('Valid until used', datetime_time_lapse))
        flow.append(('Valid until used (human readable)',
                     timestamp_to_human_readable(datetime_time_lapse)))

        signed_url = sign_url(
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            url=self.endpoint_url,
            valid_until=datetime_time_lapse
        )

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        validation_result = validate_signed_request_data(
            data=request_data,
            secret_key=self.secret_key
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    def test_02_sign_url_and_validate_signed_request_data_fail(self):
        """Fail tests for `sign_url` & `validate_signed_request_data`."""
        flow = []
        for signature_cls in self.signature_classes:
            flow += \
                self.__test_sign_url_validate_signed_request_data_fail(
                    signature_cls=signature_cls
                )
        return flow

    @log_info
    def __test_signature_to_dict_validate_signed_request_data(
            self, signature_cls=Signature):
        """
        Tests for `signature_to_dict` & `validate_signed_request_data`."""
        flow = []

        flow.append(('Signature class', signature_cls))

        signature_dict = signature_to_dict(
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            signature_cls=signature_cls
        )

        flow.append(('Dictionary created', signature_dict))

        # Now validate the signature data

        validation_result = validate_signed_request_data(
            data=signature_dict,
            secret_key=self.secret_key,
            signature_cls=signature_cls
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    def test_03_signature_to_dict_and_validate_signed_request_data(self):
        """Tests for `signature_to_dict` & `validate_signed_request_data`."""
        flow = []
        for signature_cls in self.signature_classes:
            flow += \
                self.__test_signature_to_dict_validate_signed_request_data(
                    signature_cls=signature_cls
                )
        return flow


class ExtraTest(unittest.TestCase):
    """Test for extra data."""

    def setUp(self):
        """Set up."""
        self.auth_user = 'user'
        self.secret_key = 'secret'
        self.endpoint_url = 'http://e.com/api/'
        self.signature_classes = (
            HMACMD5Signature,
            HMACSHA1Signature,
            HMACSHA224Signature,
            HMACSHA256Signature,
            HMACSHA384Signature,
            HMACSHA512Signature,
        )

    def __get_signed_url(self, signature_cls=Signature):
        """Get signed URL."""
        return sign_url(
            auth_user=self.auth_user,
            secret_key=self.secret_key,
            url=self.endpoint_url,
            extra={
                'provider': 'service1.example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john.doe@mail.example.com',
            },
            signature_cls=signature_cls
        )

    @log_info
    def __test_sign_url_validate_signed_request_data(
            self, signature_cls=Signature):
        """Tests for `sign_url` & `validate_signed_request_data`."""
        flow = []

        flow.append(('Signature class', signature_cls))

        signed_url = self.__get_signed_url(signature_cls=signature_cls)

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        # request_data['extra'] = 'provider,first_name'

        validation_result = validate_signed_request_data(
            data=request_data,
            secret_key=self.secret_key,
            signature_cls=signature_cls
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    def test_01_sign_url_and_validate_signed_request_data(self):
        """Tests for ``sign_url`` and ``validate_signed_request_data``."""
        flow = []
        for signature_cls in self.signature_classes:
            flow += self.__test_sign_url_validate_signed_request_data(
                signature_cls=signature_cls
            )
        return flow

    @log_info
    def __t_sign_url_validate_sgnd_req_data_tamper_extra_keys_rm(
            self, signature_cls=Signature):
        """Fail tests for `sign_url` and `validate_signed_request_data`.

        As well as providing the additional data ``extra`` and data tampering
        ``extra`` keys (remove).
        """
        flow = []

        flow.append(('Signature class', signature_cls))

        signed_url = self.__get_signed_url(signature_cls=signature_cls)

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        # *******************************************************************
        # ************************ Tampering ********************************
        # *******************************************************************
        tampered_request_data = copy(request_data)

        tampered_request_data['extra'] = 'provider,first_name'

        flow.append(('Request data', request_data))
        flow.append(('Tampered request data', tampered_request_data))

        validation_result = validate_signed_request_data(
            data=tampered_request_data,
            secret_key=self.secret_key,
            signature_cls=signature_cls
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    def test_02_sign_url_validate_signed_req_data_tamper_extra_keys_rm(self):
        """Fail tests for `sign_url` and `validate_signed_request_data`.

        As well as providing the additional data `extra` and data tampering
        `extra` keys (remove).
        """
        flow = []
        for signature_cls in self.signature_classes:
            flow += \
                self.__t_sign_url_validate_sgnd_req_data_tamper_extra_keys_rm(
                    signature_cls=signature_cls
                )
        return flow

    @log_info
    def __t_sgn_url_and_vldt_sgnd_req_data_tamper_extra_keys_add(
            self, signature_cls=Signature):
        """Fail tests for `sign_url` and `validate_signed_request_data`.

        As well as providing the additional data ``extra`` and data tampering
        `extra` keys (add).
        """
        flow = []

        flow.append(('Signature class', signature_cls))

        signed_url = self.__get_signed_url(signature_cls=signature_cls)

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        request_data = parse_url_params(signed_url)

        # *******************************************************************
        # ************************* Tampering *******************************
        # *******************************************************************
        tampered_request_data = copy(request_data)

        tampered_request_data['extra'] += ',age'
        tampered_request_data['age'] = 27

        flow.append(('Request data', request_data))
        flow.append(('Tampered request data', tampered_request_data))

        validation_result = validate_signed_request_data(
            data=tampered_request_data,
            secret_key=self.secret_key,
            signature_cls=signature_cls
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(not validation_result.result)

        return flow

    def test_03_sign_url_and_validate_signed_req_data_tamper_extra_keys_add(
            self):
        """Fail tests for `sign_url` and `validate_signed_request_data`.

        As well as providing the additional data ``extra`` and data tampering
        `extra` keys (add).
        """
        flow = []
        for signature_cls in self.signature_classes:
            flow += \
                self.__t_sgn_url_and_vldt_sgnd_req_data_tamper_extra_keys_add(
                    signature_cls=signature_cls
                )
        return flow

    @log_info
    def __t_sgn_url_and_vldt_sgnd_req_data_tamper_extra_keys_add(
            self, signature_cls=Signature):
        """Tests for `sign_url` and `validate_signed_request_data`.

        As well as providing the additional data `extra` and data
        tampering `extra` keys (add) repeated params.
        """
        flow = []

        flow.append(('Signature class', signature_cls))

        signed_url = "{0}&provider=cervice0.example.com".format(
            self.__get_signed_url(signature_cls=signature_cls)
        )

        # *******************************************************************
        # ************************* Tampering *******************************
        # *******************************************************************

        flow.append(('URL generated', signed_url))

        # Now parsing back the URL params and validate the signature data
        tampered_request_data = parse_url_params(signed_url)

        # *******************************************************************
        # ************************** Tampering ******************************
        # *******************************************************************
        even_more_tampered_request_data = copy(tampered_request_data)
        even_more_tampered_request_data['extra'] += ',provider'

        flow.append(('Tampered request data', tampered_request_data))
        flow.append(('Even more tampered request data',
                     even_more_tampered_request_data))

        validation_result = validate_signed_request_data(
            data=even_more_tampered_request_data,
            secret_key=self.secret_key,
            signature_cls=signature_cls
        )

        flow.append(('Signature is valid', validation_result.result))
        flow.append(('Reason not valid', validation_result.reason))

        self.assertTrue(validation_result.result)

        return flow

    def test_04_sgn_url_vldt_signed_request_data_tamper_extra_keys_add(self):
        """Tests for `sign_url` and `validate_signed_request_data`.

        As well as providing the additional data `extra` and data tampering
        `extra` keys (add) repeated params.
        """
        flow = []
        for signature_cls in self.signature_classes:
            flow += \
                self.__t_sgn_url_and_vldt_sgnd_req_data_tamper_extra_keys_add(
                    signature_cls=signature_cls
                )
        return flow


if __name__ == "__main__":
    # Tests
    unittest.main()
