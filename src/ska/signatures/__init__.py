__title__ = 'ska.signatures'
__author__ = 'Artur Barseghyan'
__copyright__ = 'Copyright (c) 2013-2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'Signature', 'HMACMD5Signature', 'HMACSHA1Signature', 'HMACSHA224Signature',
    'HMACSHA256Signature', 'HMACSHA384Signature', 'HMACSHA512Signature'
    )

from ska.signatures.hmac_md5 import HMACMD5Signature
from ska.signatures.hmac_sha1 import HMACSHA1Signature
from ska.signatures.hmac_sha224 import HMACSHA224Signature
from ska.signatures.hmac_sha256 import HMACSHA256Signature
from ska.signatures.hmac_sha384 import HMACSHA384Signature
from ska.signatures.hmac_sha512 import HMACSHA512Signature

# Default
Signature = HMACSHA1Signature
