from __future__ import absolute_import

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Signature

__title__ = 'ska.contrib.django.ska.admin'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2013-2019 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('SignatureAdmin',)


class SignatureAdmin(admin.ModelAdmin):
    """Signature admin."""

    list_display = ('signature', 'auth_user', 'valid_until', 'created',)
    readonly_fields = ('created',)
    list_filter = ('auth_user',)
    fieldsets = (
        (None, {
            'fields': ('signature', 'auth_user', 'valid_until')
        }),
        (_('Additional'), {
            'classes': ('collapse',),
            'fields': ('created',)
        }),
    )

    class Meta(object):
        """Meta class."""

        app_label = _('Signature')


admin.site.register(Signature, SignatureAdmin)
