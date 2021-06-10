# coding=utf-8
from __future__ import unicode_literals

import uuid

from factory import Faker as OriginalFaker
from faker.providers.phone_number import Provider as PhoneNumberProvider
from faker.providers.internet import Provider as InternetProvider
from faker.providers.person import Provider as PersonProvider
from faker.providers.company import Provider as CompanyProvider

localized = True

__all__ = (
    "ASCIIInternetProvider",
    "Faker",
    "MaxLengthPersonProvider",
    "NLPhoneNumberProvider",
    "UniqueCompanyProvider",
)


class Faker(OriginalFaker):
    """Override to change the default locale."""

    _DEFAULT_LOCALE = "nl_NL"


class NLPhoneNumberProvider(PhoneNumberProvider):
    """Phone number provider `compatible django.contrib.localflavor.nl`."""

    # NLPhoneNumberField validates with max=12
    formats = ("### ### ####", "##########", "###-#######", "+31#########")

    @classmethod
    def dutch_phone_number(cls):
        return cls.numerify(cls.random_element(cls.formats))


Faker.add_provider(NLPhoneNumberProvider)


class ASCIIInternetProvider(InternetProvider):
    """Internet provider which results no unicode errors."""

    def _convert_to_ascii(self, val):
        for search, replace in self.replacements:
            val = val.replace(search, replace)

        return val.encode("ascii", "ignore").decode("utf8")

    def ascii_email(self):
        pattern = self.random_element(self.email_formats)
        return self._convert_to_ascii(
            "".join(self.generator.parse(pattern).split(" "))
        )

    def ascii_safe_email(self):
        return self._convert_to_ascii(
            self.user_name()
            + "@example."
            + self.random_element(self.safe_email_tlds)
        )

    def ascii_free_email(self):
        return self._convert_to_ascii(
            self.user_name() + "@" + self.free_email_domain()
        )

    def ascii_company_email(self):
        return self._convert_to_ascii(
            self.user_name() + "@" + self.domain_name()
        )

    def ascii_uuid4_email(self):
        return self._convert_to_ascii(
            str(uuid.uuid4()) + "@" + self.domain_name()
        )


Faker.add_provider(ASCIIInternetProvider)


class MaxLengthPersonProvider(PersonProvider):
    """Person provider with safe (for Django user model) value length."""

    @classmethod
    def _max_length(cls, val, max_length=30):
        """Truncates a string given to a maximum number of characters."""
        return val[:max_length]

    @classmethod
    def first_name_max_length_30(cls):
        return cls._max_length(cls.random_element(cls.first_names))

    @classmethod
    def last_name_max_length_30(cls):
        return cls._max_length(cls.random_element(cls.last_names))


Faker.add_provider(MaxLengthPersonProvider)


class UniqueCompanyProvider(CompanyProvider):
    """Unique company provider."""

    def unique_company(self, max_length=255):
        """
        :example 'Acme Ltd'
        """
        unique_hash = str(uuid.uuid4())
        company = self.company()
        company_length = len(company)
        unique_hash_length = len(unique_hash)
        cut_chars = max_length - company_length - unique_hash_length
        return company[0:cut_chars] + unique_hash


Faker.add_provider(UniqueCompanyProvider)
