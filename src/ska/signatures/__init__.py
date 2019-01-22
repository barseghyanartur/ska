from ..signatures.hmac_md5 import HMACMD5Signature
from ..signatures.hmac_sha1 import HMACSHA1Signature
from ..signatures.hmac_sha224 import HMACSHA224Signature
from ..signatures.hmac_sha256 import HMACSHA256Signature
from ..signatures.hmac_sha384 import HMACSHA384Signature
from ..signatures.hmac_sha512 import HMACSHA512Signature

__title__ = 'ska.signatures'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'Signature',
    'HMACMD5Signature',
    'HMACSHA1Signature',
    'HMACSHA224Signature',
    'HMACSHA256Signature',
    'HMACSHA384Signature',
    'HMACSHA512Signature',
)

# Default
Signature = HMACSHA1Signature
