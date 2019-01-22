import hashlib
import hmac

from ..base import AbstractSignature

__title__ = 'ska.signatures.hmac_sha1'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('HMACSHA1Signature',)


class HMACSHA1Signature(AbstractSignature):
    """HMAC SHA-1 signature."""

    @classmethod
    def make_hash(cls, auth_user, secret_key, valid_until=None, extra=None):
        """Make hash.

        :param str auth_user:
        :param str secret_key:
        :param float|str valid_until: Unix timestamp, valid until.
        :param dict extra: Additional variables to be added.
        :return str:
        """
        if not extra:
            extra = {}

        raw_hmac = hmac.new(
            cls.make_secret_key(secret_key),
            cls.get_base(auth_user, valid_until, extra=extra),
            hashlib.sha1
        ).digest()

        return raw_hmac
