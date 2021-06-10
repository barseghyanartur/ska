from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2013-2021 Artur Barseghyan"
__license__ = "GPL 2.0/LGPL 2.1"
__all__ = ("Signature",)


class Signature(models.Model):
    """Signature.

    :Properties:
        - `signature` (str): Signature generated.
        - `auth_user` (str): Auth user.
        - `valid_until` (datetime.datetime): Valid until.
        - `created` (datetime.datetime): Time added.
    """

    signature = models.CharField(_("Signature"), max_length=255)
    auth_user = models.CharField(_("Auth user"), max_length=255)
    valid_until = models.DateTimeField(_("Valid until"))
    created = models.DateTimeField(_("Date created"), default=timezone.now)

    class Meta:
        """Meta class."""

        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        unique_together = (("signature", "auth_user", "valid_until"),)

    def __str__(self):
        return f"{self.signature}{self.auth_user}{self.valid_until}"
