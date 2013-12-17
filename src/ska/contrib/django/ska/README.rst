===================================================
ska.contrib.django.ska
===================================================
Django `ska` integration.

- Model and view (including class-based views) decorators for signing and validating the URLs.
- Authentication backend for Django based on the signatures (tokens) generated using `ska`, which
  allows you to get a password-less login to Django web site.

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

Demo
===============================================
In order to be able to quickly evaluate the `ska`, a demo app (with a quick installer) has been created
(works on Ubuntu/Debian, may work on other Linux systems as well, although not guaranteed). Follow the
instructions below for having the demo running within a minute.

Grab the latest `ska_example_app_installer.sh`:

    $ wget https://raw.github.com/barseghyanartur/ska/stable/example/ska_example_app_installer.sh

Assign execute rights to the installer and run the `django_dash_example_app_installer.sh`:

    $ chmod +x ska_example_app_installer.sh

    $ ./ska_example_app_installer.sh

Open your browser and test the app.

Foo listing (ska protected views):

- URL: http://127.0.0.1:8001/foo/

Authentication page (ska authentication backend):

- URL: http://127.0.0.1:8001/foo/authenticate/

Django admin interface:

- URL: http://127.0.0.1:8001/admin/
- Admin username: test_admin
- Admin password: test

Usage and examples
===================================================
See the (https://github.com/barseghyanartur/ska/tree/stable/example) for a working example project.

Signing URLs
---------------------------------------------------
foo/models.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The following code is given as an example. Note the ``validate_signed_request`` decorator used in ``detail``
view function.

>>> from ska.contrib.django.ska.decorators import validate_signed_request
>>>
>>> # Your view that shall be protected
>>> @validate_signed_request()
>>> def detail(request, slug, template_name='foo/detail.html'):
>>>     # Your code

Authentication backend
---------------------------------------------------
Allows you to get a password-less login to Django web site. By default, number of logins using the
same token is not limited. If you wish that single tokens become invalid after first use, set
the following variables to True in your projects' Django settings module.

>>> SKA_DB_STORE_SIGNATURES = True
>>> SKA_DB_PERFORM_SIGNATURE_CHECK = True

Server side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
On the server side, where users are supposed to log in, the following shall be present.

settings.py
+++++++++++++++++++++++++++++++++++++++++++++++++++
>>> AUTHENTICATION_BACKENDS = (
>>>     'ska.contrib.django.ska.backends.SkaAuthenticationBackend',
>>>     'django.contrib.auth.backends.ModelBackend',
>>> )

>>> INSTALLED_APPS = (
>>>     # ...
>>>     'ska.contrib.django.ska',
>>>     # ...
>>> )

>>> SKA_SECRET_KEY = 'secret-key'
>>> SKA_UNAUTHORISED_REQUEST_ERROR_TEMPLATE = 'ska/401.html'
>>> SKA_REDIRECT_AFTER_LOGIN = '/foo/logged-in/'

urls.py
+++++++++++++++++++++++++++++++++++++++++++++++++++
>>> urlpatterns = patterns('',
>>>     url(r'^ska/', include('ska.contrib.django.ska.urls')),
>>>     url(r'^admin/', include(admin.site.urls)),
>>> )

Purging of old signature data
+++++++++++++++++++++++++++++++++++++++++++++++++++
If you have lots of visitors and the ``SKA_DB_STORE_SIGNATURES`` set to True, your database
grows. If you wish to get rid of old signature token data, you may want to execute the following
command using a cron job.

    $ ./manage.py ska_purge_stored_signature_data

Client side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
On the client application side, the only thing that shall be present is the `ska` module for Django and
of course the same ``SECRET_KEY`` as on the server side. Further, the server `ska` login URL (in our case
"/ska/login/") shall be signed using `ska` (for example, using `sign_url` function). The `auth_user` param
would be used as a Django username. See the example below.

>>> from ska import sign_url
>>> from ska.contrib.django.ska.settings import SECRET_KEY
>>>
>>> server_ska_login_url = 'https://server-url.com/ska/login/'
>>>
>>> signed_url = sign_url(
>>>     auth_user = 'test_ska_user_0',
>>>     secret_key = SECRET_KEY,
>>>     url = server_ska_login_url
>>>     )

Put this code, for instance, put it to your template context and show to the user for authenticating to
the server.

>>> def auth_to_server(request, template_name='auth_to_server.html'):
>>>     # Some code + obtaining the `signed_url` (code shown above)
>>>     context = {
>>>         'signed_url': signed_url,
>>>     }
>>>
>>>     return render_to_response(
>>>         template_name,
>>>         context,
>>>         context_instance = RequestContext(request)
>>>         )

Security notes
+++++++++++++++++++++++++++++++++++++++++++++++++++
From point of security, you should be serving the following pages via HTTP secure connection:

- The server login page (/ska/login/).
- The client page containing the authentication links.

License
===================================================
GPL 2.0/LGPL 2.1

Support
===================================================
For any issues contact me at the e-mail given in the `Author` section.

Author
===================================================
Artur Barseghyan <artur.barseghyan@gmail.com>
