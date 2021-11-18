import unittest

from .. import Signature, HMACSHA256Signature, HMACSHA512Signature
from ..helpers import (
    sorted_urlencode,
    javascript_quoter,
    javascript_value_dumper,
)

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
        """Test `get_base`.

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

    def test_signature_to_dict(self):
        """Test `signature_to_dict`."""

        # Test case 1
        signature1 = Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature1 = b"WTjN2wPENDW1gCHEVPKz3IXlE0g="
        self.assertEqual(signature1.signature, expected_signature1)

        # Test case 2
        signature2 = Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={"one": "1", "two": "2"},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature2 = b"dFqd/VbWOaY3ROlL89K6JZZsfhE="
        self.assertEqual(signature2.signature, expected_signature2)

        # Test case 3
        signature3 = Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={"one": "â"},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature3 = b"dlT2WO/jYq7+xcvDEUkCnNW5TxA="
        self.assertEqual(signature3.signature, expected_signature3)

        # Test case 4
        signature4 = Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={"one": {"value": "â"}},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature4 = b"+pA63D4EMF2pcfIlE/dYXyNkhx4="
        self.assertEqual(signature4.signature, expected_signature4)

        # Test case 11
        signature11 = HMACSHA256Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature11 = b"EZ7uXeeopIxK3wL62J/9tKPXoGmNk9V3KHGgwge9/ek="
        self.assertEqual(signature11.signature, expected_signature11)

        # Test case 12
        signature12 = HMACSHA256Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={"one": "1", "two": "2"},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature12 = b"Cl90LfQ2L3DW2MAhZriqCfEisPdL+1aHA/M0GPc1Yr4="
        self.assertEqual(signature12.signature, expected_signature12)

        # Test case 13
        signature13 = HMACSHA256Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={"one": "â"},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature13 = b"9UpLTlFgEbCJ2C4/gC4eDogn0JiuMzo7osbMEOejwkQ="
        self.assertEqual(signature13.signature, expected_signature13)

        # Test case 14
        signature14 = HMACSHA256Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={"one": {"value": "â"}},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature14 = b"9Tg3PdJYm/2tKZtVU0F/5T6TtL39Rwy4Uniq36ZClMY="
        self.assertEqual(signature14.signature, expected_signature14)

        # Test case 21
        signature21 = HMACSHA512Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature21 = b"7QcInLFxLrv1TeZZY4EXbAc1YguBlcjmYfFe5J+FH4TAOquSBZvKwYLSQCS4VVmdhDDU1h1zVlPDc4MAW6SHGQ=="
        self.assertEqual(signature21.signature, expected_signature21)

        # Test case 22
        signature22 = HMACSHA512Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={"one": "1", "two": "2"},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature22 = b"+Bm5xtd3Cl+7VV0RM6H14z68M8vWuMP168m3UsXLP1jHTTQCg3mXxTncZ9a57AoQefh/qNmDdnD5AmFYGzJ+PQ=="
        self.assertEqual(signature22.signature, expected_signature22)

        # Test case 23
        signature23 = HMACSHA512Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={"one": "â"},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature23 = b"yockrWxDncGJ2/HMEi/ma/auEmv8xlIMm5U50CuTFYSKbzrgNPh4OXgax/s2d96+paaLagwmnZK1+xUGHeArXw=="
        self.assertEqual(signature23.signature, expected_signature23)

        # Test case 24
        signature24 = HMACSHA512Signature.generate_signature(
            AUTH_USER,
            SECRET_KEY,
            VALID_UNTIL,
            extra={"one": {"value": "â"}},
            value_dumper=javascript_value_dumper,
            quoter=javascript_quoter,
        )
        expected_signature24 = b"OlFZzu/SlBQYWny3CVvP7ghiL6X8G4r/yS9yNl8N+9b1arae3AkMLCp+0MuLs2sp8qdM3j+a7MYdCQCBSOnAoQ=="
        self.assertEqual(signature24.signature, expected_signature24)
