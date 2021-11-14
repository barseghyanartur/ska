import unittest

from .. import Signature
from ..helpers import sorted_urlencode, javascript_quoter, javascript_value_dumper

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = (
    "IntegrationTest",
)

SECRET_KEY = "UxuhnPaO4vKA"

AUTH_USER = "me@example.com"

VALID_UNTIL = "1628717009.0"


class IntegrationTest(unittest.TestCase):
    """Integration tests.

    Supposed to be in sync with some specific `skajs` and `skaphp` cases.
    """

    def test_get_base(self, signature_cls=Signature):
        """
        // Test case 1
        $base = getBase(AUTH_USER, VALID_UNTIL, null);
        $expectedBase = "1628717009.0_me@example.com";
        self::assertEquals($base, $expectedBase);

        // Test case 2
        $base2 = getBase(AUTH_USER, VALID_UNTIL, ["one" => "1", "two" => "2"]);
        $expectedBase2 = "1628717009.0_me@example.com_one%3D1%26two%3D2";
        self::assertEquals($base2, $expectedBase2);

        // Test case 3
        const base3 = getBase(AUTH_USER, validUntil, {"one": "â"}, encodedValueDumper);
        const expectedBase3 = "1628717009.0_me@example.com_one%3D%C3%A2";
        t.is(base3, expectedBase3);

        // Test case 4
        const base4 = getBase(AUTH_USER, validUntil, {"one": {"value": "â"}}, encodedValueDumper);
        const expectedBase4 = "1628717009.0_me@example.com_one%3D%7B%22value%22%3A%22%5Cu00e2%22%7D";
        t.is(base4, expectedBase4);
        """

        # Test case 1
        base1 = signature_cls.get_base(
            AUTH_USER,
            VALID_UNTIL,
            {}
        )
        expected_base1 = b"1628717009.0_me@example.com"
        self.assertEqual(base1, expected_base1)

        # Test case 2
        base2 = signature_cls.get_base(
            AUTH_USER,
            VALID_UNTIL,
            {"one": "1", "two": "2"}
        )
        expected_base2 = b"1628717009.0_me@example.com_one%3D1%26two%3D2"
        self.assertEqual(base2, expected_base2)

        # Test case 3
        base3 = signature_cls.get_base(
            AUTH_USER,
            VALID_UNTIL,
            {"one": "â"},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter
        )
        expected_base3 = b"1628717009.0_me@example.com_one%3D%C3%A2"
        self.assertEqual(base3, expected_base3)

        # Test case 4
        base4 = signature_cls.get_base(
            AUTH_USER,
            VALID_UNTIL,
            {"one": {"value": "â"}},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter
        )
        expected_base4 = b"1628717009.0_me@example.com_one%3D%7B%22value%22%3A%22%5Cu00e2%22%7D"
        self.assertEqual(base4, expected_base4)

    def test_sorted_urlencode(self, signature_cls=Signature):
        """Test `sorted_urlencode`."""
        # Test case 5 - Encoded simple unicode data quoted
        encoded_data = sorted_urlencode(
            {"one": "â"},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_data = "one%3D%C3%A2"
        self.assertEqual(encoded_data, expected_data)

        # Test case 6 - Encoded simple unicode data unquoted
        encoded_data = sorted_urlencode(
            {"one": "â"},
            quoted=False,
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_data = "one=â"
        self.assertEqual(encoded_data, expected_data)

        # Test case 7 - Encoded complex unicode data quoted
        encoded_data = sorted_urlencode(
            {"one": {"value": "â"}},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_data = "one%3D%7B%22value%22%3A%22%5Cu00e2%22%7D"
        self.assertEqual(encoded_data, expected_data)

        # Test case 8 - Encoded complex unicode data quoted
        encoded_data = sorted_urlencode(
            {"one": {"value": "â"}},
            quoted=False,
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_data = 'one={"value":"\\u00e2"}'
        self.assertEqual(encoded_data, expected_data)
