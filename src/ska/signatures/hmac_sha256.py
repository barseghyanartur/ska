import hashlib
import hmac
from typing import Union, Optional, Dict, Callable

from ..base import AbstractSignature

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("HMACSHA256Signature",)


class HMACSHA256Signature(AbstractSignature):
    """HMAC SHA-256 signature."""

    @classmethod
    def make_hash(
        cls,
        auth_user: str,
        secret_key: str,
        valid_until: Union[str, float] = None,
        extra: Optional[Dict[str, Union[bytes, str, float, int]]] = None,
        value_dumper: Optional[Callable] = None,
        quoter: Optional[Callable] = None,
    ) -> bytes:
        """Make hash.

        You should implement this method in your signature class.

        :param auth_user:
        :param secret_key:
        :param valid_until: Unix timestamp, valid until.
        :param extra: Additional variables to be added.
        :param value_dumper:
        :param quoter:
        :return:
        """
        if not extra:
            extra = {}

        raw_hmac = hmac.new(
            cls.make_secret_key(secret_key),
            cls.get_base(
                auth_user,
                valid_until,
                extra=extra,
                value_dumper=value_dumper,
                quoter=quoter,
            ),
            hashlib.sha256,
        ).digest()

        return raw_hmac
