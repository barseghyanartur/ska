from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse

from ska.contrib.django.ska.decorators import sign_url

class FooItem(models.Model):
    """
    Foo item.

    ``title`` Title of the foo item.
    ``slug`` URL slug of the foo item.
    ``body`` Teaser of the foo item.
    """
    title = models.CharField(_("Title"), max_length=100)
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    body = models.TextField(_("Body"))

    class Meta:
        verbose_name = _("Foo item")
        verbose_name_plural = _("Foo items")

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        """
        Absolute URL, which goes to the foo item detail page.

        :return str:
        """
        return reverse('foo.detail', kwargs={'slug': self.slug})

    @sign_url()
    def get_signed_absolute_url(self):
        """
        Absolute URL, which goes to the foo item detail page.

        :return str:
        """
        return reverse('foo.detail', kwargs={'slug': self.slug})
    get_signed_absolute_url.allow_tags = True
    get_signed_absolute_url.short_description = _('Signed URL')

    @sign_url(extra={'email': 'john.doe@mail.example.com', 'first_name': 'John', 'last_name': 'Doe', 'age': 64})
    def get_signed_class_based_absolute_url(self):
        """
        Absolute URL, which goes to the foo item detail page. Note, that we add extra params here.
        When authenticating using this URLs, user would have the information shown saved into his profile.
        This is given purely as example. Normally, you wouldn't be adding emails and other user data in
        such a way, however - it's a very quick way of showing how it works.

        :return str:
        """
        return reverse('foo.class-based.detail', kwargs={'slug': self.slug})
    get_signed_absolute_url.allow_tags = True
    get_signed_absolute_url.short_description = _('Signed URL')
