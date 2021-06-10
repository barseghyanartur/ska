from django.core.management.base import BaseCommand

from ska.contrib.django.ska.tests import create_admin_user, generate_data

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("Command",)


class Command(BaseCommand):
    """Purges old signature data (valid_until < now)."""

    def handle(self, *args, **options):
        """Handle."""
        create_admin_user()
        generate_data()
