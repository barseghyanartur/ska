from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from ska.contrib.django.ska.decorators import sign_url

__all__ = (
    "FooItem",
    "FooItemConstanceProviderSignedRequestRequired",
    "FooItemConstanceSignedRequestRequired",
    "FooItemProviderSignedRequestRequired",
    "FooItemSignedRequestRequired",
)


class FooItem(models.Model):
    """Foo item.

    ``title`` Title of the foo item.
    ``slug`` URL slug of the foo item.
    ``body`` Teaser of the foo item.
    """

    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    body = models.TextField(_("Body"))

    class Meta:
        """Meta."""

        verbose_name = _("Foo item")
        verbose_name_plural = _("Foo items")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Absolute URL, which goes to the foo item detail page.

        :return str:
        """
        return reverse("foo.detail", kwargs={"slug": self.slug})

    def get_cbv_absolute_url(self):
        """Absolute URL, which goes to the foo item detail page.

        :return str:
        """
        return reverse("foo.class-based.detail", kwargs={"slug": self.slug})

    @sign_url()
    def get_signed_absolute_url(self):
        """Absolute URL, which goes to the foo item detail page.

        :return str:
        """
        return reverse("foo.detail", kwargs={"slug": self.slug})

    get_signed_absolute_url.allow_tags = True
    get_signed_absolute_url.short_description = _("Signed URL")

    @sign_url(
        extra={
            "email": "john.doe@mail.example.com",
            "first_name": "John",
            "last_name": "Doe",
            "age": 64,
        }
    )
    def get_signed_class_based_absolute_url(self):
        """Absolute URL, which goes to the foo item detail page.

        Note, that we add extra params here. When authenticating using this
        URLs, user would have the information shown saved into his profile.
        This is given purely as example. Normally, you wouldn't be adding
        emails and other user data in such a way, however - it's a very
        quick way of showing how it works.

        :return str:
        """
        return reverse("foo.class-based.detail", kwargs={"slug": self.slug})

    get_signed_absolute_url.allow_tags = True
    get_signed_absolute_url.short_description = _("Signed URL")


class FooItemSignedRequestRequired(FooItem):
    class Meta:
        proxy = True


class FooItemProviderSignedRequestRequired(FooItem):
    class Meta:
        proxy = True


class FooItemConstanceSignedRequestRequired(FooItem):
    class Meta:
        proxy = True


class FooItemConstanceProviderSignedRequestRequired(FooItem):
    class Meta:
        proxy = True
