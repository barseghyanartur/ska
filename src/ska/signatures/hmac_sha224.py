import hashlib
import hmac
from typing import Union, Optional, Dict

from ..base import AbstractSignature

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("HMACSHA224Signature",)


class HMACSHA224Signature(AbstractSignature):
    """HMAC SHA-224 signature."""

    @classmethod
    def make_hash(
        cls,
        auth_user: str,
        secret_key: str,
        valid_until: Union[str, float] = None,
        extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
    ) -> bytes:
        """Make hash.

        You should implement this method in your signature class.

        :param auth_user:
        :param secret_key:
        :param valid_until: Unix timestamp, valid until.
        :param extra: Additional variables to be added.
        :return:
        """
        if not extra:
            extra = {}

        raw_hmac = hmac.new(
            cls.make_secret_key(secret_key),
            cls.get_base(auth_user, valid_until, extra=extra),
            hashlib.sha224,
        ).digest()

        return raw_hmac
