===================================================
ska.contrib.django.ska
===================================================

Prerequisites
===================================================
- Python 2.6.8+, 2.7.+, 3.3.+
- Django 1.5.+

Installation and configuration
===================================================
1. Install `ska`
---------------------------------------------------
Latest stable version from PyPI.

    $ pip install ska

Latest stable version from bitbucket.

    $ pip install -e hg+https://bitbucket.org/barseghyanartur/ska@stable#egg=ska

Latest stable version from github.

    $ pip install -e git+https://github.com/barseghyanartur/ska@stable#egg=ska

2. Configure `ska` (settings.py)
---------------------------------------------------
- Add 'ska.contrib.django.ska' to ``INSTALLED_APPS`` of your projects' `settings` module.

>>> INSTALLED_APPS = (
>>>     # ...
>>>     'ska.contrib.django.ska'
>>>     #
>>> )

- Define ``SKA_SECRET_KEY`` variable in your projects' `settings` module.

>>> SKA_SECRET_KEY = 'my-secret-key'

- If you wish to have a HTML template for 401 errors (unauthorised), provide a path to your `401.html`
  template in ``SKA_UNAUTHORISED_REQUEST_ERROR_TEMPLATE`` variable in your projects' `settings` module.
  Take `ska/contrib/django/ska/templates/ska/401.html` as an example.

>>> SKA_UNAUTHORISED_REQUEST_ERROR_TEMPLATE = 'ska/401.html'

Usage and examples
===================================================
See the (https://github.com/barseghyanartur/ska/tree/stable/example) for a working example project.

foo/models.py
---------------------------------------------------
The following code is given as an example. Note the ``sign_url`` decorator used in ``get_signed_absolute_url``
method.

>>> from django.db import models
>>> from django.utils.translation import ugettext_lazy as _
>>> from django.core.urlresolvers import reverse
>>>
>>> from ska.contrib.django.ska.decorators import sign_url
>>>
>>> class FooItem(models.Model):
>>>     title = models.CharField(_("Title"), max_length=100)
>>>     slug = models.SlugField(unique=True, verbose_name=_("Slug"))
>>>     body = models.TextField(_("Body"))
>>>
>>>     # Unsigned absolute URL, which goes to the foo item detail page.
>>>     def get_absolute_url(self):
>>>         return reverse('foo.detail', kwargs={'slug': self.slug})
>>>
>>>     # Signed absolute URL, which goes to the foo item detail page.
>>>     @sign_url()
>>>     def get_signed_absolute_url(self):
>>>         return reverse('foo.detail', kwargs={'slug': self.slug})

foo/views.py
---------------------------------------------------
The following code is given as an example. Note the ``validate_signed_request`` decorator used in ``detail``
view function.

>>> from ska.contrib.django.ska.decorators import validate_signed_request
>>>
>>> # Your view that shall be protected
>>> @validate_signed_request()
>>> def detail(request, slug, template_name='foo/detail.html'):
>>>     # Your code

License
===================================================
GPL 2.0/LGPL 2.1

Support
===================================================
For any issues contact me at the e-mail given in the `Author` section.

Author
===================================================
Artur Barseghyan <artur.barseghyan@gmail.com>
