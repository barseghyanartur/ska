__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2013 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('Signature',)

import logging

from django.db import models
from django.utils.translation import ugettext_lazy as _

logger = logging.getLogger(__name__)

class Signature(models.Model):
    """
    Token

    :Properties:
        - `signature` (str): Signature generated.
        - `auth_user` (str): Auth user.
        - `valid_until` (datetime.datetime): Valid until.
        - `created` (datetime.datetime): Time added.
    """
    signature = models.CharField(_("Signature"), max_length=255)
    auth_user = models.CharField(_("Auth user"), max_length=255)
    valid_until = models.DateTimeField(_("Valid until"))
    created = models.DateTimeField(_("Date created"), auto_now_add=True)

    class Meta:
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")
        unique_together = (('signature', 'auth_user', 'valid_until'),)

    def __unicode__(self):
        return "{0}{1}{2}".format(self.signature, self.auth_user, self.valid_until)
