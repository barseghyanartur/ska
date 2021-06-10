from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import FooItem


class FooItemAdmin(admin.ModelAdmin):
    """Foo item admin."""

    list_display = ("title",)

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        (None, {"fields": ("title", "slug", "body")}),
        # (_("Additional"), {
        #    'classes': ('collapse',),
        #    'fields': ('date_created', 'date_updated')
        # })
    )

    class Meta:
        """Meta."""

        app_label = _("Foo item")


admin.site.register(FooItem, FooItemAdmin)
