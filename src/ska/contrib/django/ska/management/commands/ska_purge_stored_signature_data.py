__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('Command',)

from django.core.management.base import BaseCommand

from ska.contrib.django.ska.utils import purge_signature_data

class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Purges old signature data (valid_until < now).
        """
        purge_signature_data()
