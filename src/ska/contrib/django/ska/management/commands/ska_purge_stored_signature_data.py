from django.core.management.base import BaseCommand

from ska.contrib.django.ska.utils import purge_signature_data

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2023 Artur Barseghyan"
__license__ = "GPL-2.0-only OR LGPL-2.1-or-later"
__all__ = ("Command",)


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        Purges old signature data (valid_until < now).
        """
        purge_signature_data()
