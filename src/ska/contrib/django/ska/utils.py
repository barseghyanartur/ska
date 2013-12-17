__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('purge_signature_data',)

import datetime

from ska.contrib.django.ska.models import Signature

def purge_signature_data():
    """
    Purges old signature data (valid_until < now).
    """
    Signature._default_manager.filter(valid_until__lt=datetime.datetime.now()).delete()
