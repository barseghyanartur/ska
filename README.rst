===================================================
ska
===================================================
Lets you easily generate signatures for signing (HTTP) requests, using symmetric-key algorithm encryption.
Allows you to validate signed requests and identify possible validation errors. Uses sha1/hmac for
signature encryption.

Key concepts
===================================================
Host and server share the Secret Key, which is used to sign requests. Secret key is never sent around.

Each (HTTP) request is signed on the client side using the shared Secret Key and as an outcome produces
the triple (``signature``, ``auth_user``, ``valid_until``) which are used to sign the requests.

- `signature` (str): Signature generated.
- `auth_user` (str): User making the request. Can be anything.
- `valid_until` (float|str): Signature expiration time (Unix timestamp).

On the server side, (HTTP) request is validated using the shared Secret Key. It's being checked
whether signature is valid and not expired.

Features
===================================================
Core `ska` module
---------------------------------------------------
- Sign URLs.
- Validate URLs.

Django `ska` module (`ska.contrib.django.ska`)
---------------------------------------------------
- Model and view (including class-based views) decorators for signing and validating the URLs.
- Authentication backend for Django based on the signatures (tokens) generated using `ska`, which
  allows you to get a password-less login to Django web site.

Prerequisites
===================================================
- Core `ska` module requires Python 2.6.8+, 2.7.+, 3.3.+
- Django `ska` module (`ska.contrib.django.ska`) requires the mentioned above plus Django 1.5.+

Installation
===================================================
Latest stable version from PyPI.

    $ pip install ska

Latest stable version from bitbucket.

    $ pip install -e hg+https://bitbucket.org/barseghyanartur/ska@stable#egg=ska

Latest stable version from github.

    $ pip install -e git+https://github.com/barseghyanartur/ska@stable#egg=ska

Usage examples
===================================================
For integration with Django, see the `Django integration` section.

Basic usage
---------------------------------------------------
Pure Python usage.

Client side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Signing URLs is as simple as follows.

Required imports.

>>> from ska import sign_url

Producing a signed URL.

>>> signed_url = sign_url(
>>>     auth_user='user', secret_key='your-secret_key', url='http://e.com/api/'
>>> )
http://e.com/api/?valid_until=1378045287.0&auth_user=user&signature=YlZpLFsjUKBalL4x5trhkeEgqE8%3D

Default lifetime of a signature is 10 minutes (600 seconds). If you want it to be different, provide a
``lifetime`` argument to ``sign_url`` function.

Default name of the (GET) param holding the generated signature value is `signature`. If you want it
to be different, provide a ``signature_param`` argument to ``sign_url`` function.

Default name of the (GET) param holding the ``auth_user`` value is `auth_user`. If you want it
to be different, provide a ``auth_user_param`` argument to ``sign_url`` function.

Default name of the (GET) param holding the ``valid_until`` value is `valid_until`. If you want it
to be different, provide a ``valid_until_param`` argument to ``sign_url`` function.

Note, that by default a suffix '?' is added after the given ``url`` and generated signature params.
If you want that suffix to be custom or gone, provide a ``suffix`` argument to the ``sign_url``
function.

With all customisations, it would look as follows.

>>> signed_url = sign_url(
>>>     auth_user='user', secret_key='your-secret_key', lifetime=120,
>>>     url='http://e.com/api/', signature_param='signature',
>>>     auth_user_param='auth_user', valid_until_param='valid_until'
>>> )

It's also possible to add additional data to the signature by providing a ``extra`` argument (dict).
Note, that additional data is signed as well. If request is somehow tampered (values vary from
originally provided ones), signature becomes invalid.

>>> sign_url(
>>>     auth_user = 'user', secret_key = 'your-secret_key', url = 'http://e.com/api/',
>>>     extra = {'email': 'doe@example.com', 'last_name': 'Doe', 'first_name': 'Joe'}
>>>     )

You may now proceed with the signed URL request. If you use the famous ``requests`` library, it would
be as follows.

>>> import requests
>>> requests.get(signed_url)

If you want to use POST method instead, you would likely want to get a dictionary back,
in order to append it to the POST data later.

Required imports.

>>> from ska import signature_to_dict

Producing a dictionary containing the signature data, ready to be put into the request (for
example POST) data. All customisations mentioned above for the ``sign_url`` function, also
apply to the ``signature_to_dict``.

>>> signature_dict = signature_to_dict(
>>>     auth_user='user', secret_key='your-secret_key'
>>>     )
{
    'signature': 'YlZpLFsjUKBalL4x5trhkeEgqE8=',
    'auth_user': 'user',
    'valid_until': '1378045287.0'
}

Adding of additional data to the signature works in the same way.

>>> signature_dict = signature_to_dict(
>>>     auth_user = 'user',
>>>     secret_key = 'your-secret_key',
>>>     extra = {
>>>         'email': 'john.doe@mail.example.com',
>>>         'first_name': 'John',
>>>         'last_name': 'Doe'
>>>     }
>>>     )
{
    'auth_user': 'user',
    'email': 'john.doe@mail.example.com',
    'extra': 'email,first_name,last_name',
    'first_name': 'John',
    'last_name': 'Doe',
    'signature': 'cnSoU/LnJ/ZhfLtDLzab3a3gkug=',
    'valid_until': 1387616469.0
}

If you for some reason prefer a lower level implementation, read the same section in the
`Advanced usage` chapter.

Server side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Validating the signed request data is as simple as follows.

Required imports.

>>> from ska import validate_signed_request_data

Validating the signed request data. Note, that ``data`` value is expected to be a dictionary;
``request.GET`` is given as an example. It will most likely vary from what's used in your
framework (unless you use Django).

>>> validation_result = validate_signed_request_data(
>>>     data = request.GET, # Note, that ``request.GET`` is given as example.
>>>     secret_key = 'your-secret_key'
>>> )

The ``validate_signed_request_data`` produces a ``ska.SignatureValidationResult`` object,
which holds the following data:

- `result` (bool): True if data is valid. False otherwise.
- `reason` (list): List of strings, indicating validation errors. Empty list in case if ``result``
  is True.

Default name of the (GET) param holding the signature value is `signature`. If you want it
to be different, provide a ``signature_param`` argument to ``validate_signed_request_data``
function.

Default name of the (GET) param holding the ``auth_user`` value is `auth_user`. If you want it
to be different, provide a ``auth_user_param`` argument to ``validate_signed_request_data``
function.

Default name of the (GET) param holding the ``valid_until`` value is `valid_until`. If you want it
to be different, provide a ``valid_until_param`` argument to ``validate_signed_request_data``
function.

With all customisations, it would look as follows. Note, that ``request.GET`` is given as example.

>>> validation_result = validate_signed_request_data(
>>>     data = request.GET,
>>>     secret_key = 'your-secret_key',
>>>     signature_param='signature',
>>>     auth_user_param='auth_user', \
>>>     valid_until_param='valid_until'
>>> )

If you for some reason prefer a lower level implementation, read the same section in the
`Advanced usage` chapter.

Command line usage
---------------------------------------------------
It's possible to generate a signed URL from command line using the `ska.generate_signed_url`
module.

:Arguments:

>>>  -h, --help            show this help message and exit
>>>
>>>  -au AUTH_USER, --auth-user AUTH_USER
>>>                        `auth_user` value
>>>
>>>  -sk SECRET_KEY, --secret-key SECRET_KEY
>>>                        `secret_key` value
>>>
>>>  -vu VALID_UNTIL, --valid-until VALID_UNTIL
>>>                        `valid_until` value
>>>
>>>  -l LIFETIME, --lifetime LIFETIME
>>>                        `lifetime` value
>>>
>>>  -u URL, --url URL     URL to sign
>>>
>>>  -sp SIGNATURE_PARAM, --signature-param SIGNATURE_PARAM
>>>                        (GET) param holding the `signature` value
>>>
>>>  -aup AUTH_USER_PARAM, --auth-user-param AUTH_USER_PARAM
>>>                        (GET) param holding the `auth_user` value
>>>
>>>  -vup VALID_UNTIL_PARAM, --valid-until-param VALID_UNTIL_PARAM
>>>                        (GET) param holding the `auth_user` value

:Example:

    $ python src/ska/generate_signed_url.py -au user -sk your-secret-key

Advanced usage (low-level)
---------------------------------------------------
Client side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Required imports.

>>> from ska import Signature, RequestHelper

Generate a signature.

>>> signature = Signature.generate_signature(
>>>     auth_user = 'user',
>>>     secret_key = 'your-secret-key'
>>>     )

Default lifetime of a signature is 10 minutes (600 seconds). If you want it to be different, provide a
``lifetime`` argument to ``generate_signature`` method.

>>> signature = Signature.generate_signature(
>>>     auth_user = 'user',
>>>     secret_key = 'your-secret-key',
>>>     lifetime = 120 # Signatre lifetime set to 120 seconds.
>>>     )

Your endpoint operates with certain param names and you need to wrap generated signature params into
the URL. In order to have the job done in an easy way, create a request helper. Feed names of the
(GET) params to the request helper and let it make a signed endpoint URL for you.

>>> request_helper = RequestHelper(
>>>     signature_param = 'signature',
>>>     auth_user_param = 'auth_user',
>>>     valid_until_param = 'valid_until'
>>> )

Append signature params to the endpoint URL.

>>> signed_url = request_helper.signature_to_url(
>>>     signature = signature,
>>>     endpoint_url = 'http://e.com/api/'
>>> )
http://e.com/api/?valid_until=1378045287.0&auth_user=user&signature=YlZpLFsjUKBalL4x5trhkeEgqE8%3D

Make a request.

>>> import requests
>>> r = requests.get(signed_url)

Server side
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Required imports.

>>> from ska import RequestHelper

Create a request helper. Your endpoint operates with certain param names. In order to have the job done
in an easy way, we feed those params to the request helper and let it extract data from signed request
for us.

>>> request_helper = RequestHelper(
>>>     signature_param = 'signature',
>>>     auth_user_param = 'auth_user',
>>>     valid_until_param = 'valid_until'
>>> )

Validate the request data. Note, that ``request.GET`` is given just as an example.

>>> validation_result = request_helper.validate_request_data(
>>>     data = request.GET,
>>>     secret_key = 'your-secret-key'
>>> )

Your implementation further depends on you, but may look as follows.

>>> if validation_result.result:
>>>     # Validated, proceed further
>>>     # ...
>>> else:
>>>     # Validation not passed.
>>>     raise Http404(validation_result.reason)

You can also just validate the signature by calling ``validate_signature`` method of
the ``ska.Signature``.

>>> Signature.validate_signature(
>>>     signature = 'EBS6ipiqRLa6TY5vxIvZU30FpnM=',
>>>     auth_user = 'user',
>>>     secret_key = 'your-secret-key',
>>>     valid_until = '1377997396.0'
>>>     )

Django integration
---------------------------------------------------
'ska` comes with Django model- and view-decorators for producing signed URLs and and validating the
endpoints, as well as with authentication backend, which allows password-less login into Django
web site using `ska` generated signature tokens.

Demo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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

Configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Secret key (str) must be defined in `settings` module of your project.

>>> SKA_SECRET_KEY = 'my-secret-key'

The following variables can be overridden in `settings` module of your project.

- `SKA_UNAUTHORISED_REQUEST_ERROR_MESSAGE` (str): Plain text error message. Defaults to
  "Unauthorised request. {0}".
- `SKA_UNAUTHORISED_REQUEST_ERROR_TEMPLATE` (str): Path to 401 template that should be rendered in
  case of 401
  responses. Defaults to empty string (not provided).
- `SKA_AUTH_USER` (str): The ``auth_user`` argument for ``ska.sign_url`` function. Defaults to
  "ska-auth-user".

See the (https://github.com/barseghyanartur/ska/tree/stable/example) for a working example project.

Django model method decorator ``sign_url``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is most likely be used in module `models` (models.py).

Imagine, you have a some objects listing and you want to protect the URLs to be viewed by authorised
parties only. You would then use ``get_signed_absolute_url`` method when rendering the listing (HTML).

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

Note, that ``sign_url`` decorator accepts the following optional arguments.

- `auth_user` (str): Username of the user making the request.
- `secret_key`: The shared secret key. If set, overrides the ``SKA_SECRET_KEY`` variable set in
  the `settings` module of your project.
- `valid_until` (float or str ): Unix timestamp. If not given, generated automatically (now + lifetime).
- `lifetime` (int): Signature lifetime in seconds.
- `suffix` (str): Suffix to add after the ``endpoint_url`` and before the appended signature params.
- `signature_param` (str): Name of the GET param name which would hold the generated signature value.
- `auth_user_param` (str): Name of the GET param name which would hold the ``auth_user`` value.
- `valid_until_param` (str): Name of the GET param name which would hold the ``valid_until`` value.

Django view decorator ``validate_signed_request``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To be used to protect views (file views.py). Should be applied to views (endpoints) that require
signed requests. If checks are not successful, a ``ska.contrib.django.ska.http.HttpResponseUnauthorized``
is returned, which is a subclass of Django's ``django.http.HttpResponse``. You can provide your own
template for 401 error. Simply point the ``SKA_UNAUTHORISED_REQUEST_ERROR_TEMPLATE`` in `settings`
module to the right template. See `ska/contrib/django/ska/templates/ska/401.html` as a template
example.

>>> from ska.contrib.django.ska.decorators import validate_signed_request
>>>
>>> # Your view that shall be protected
>>> @validate_signed_request()
>>> def detail(request, slug, template_name='foo/detail.html'):
>>>     # Your code

Note, that ``validate_signed_request`` decorator accepts the following optional arguments.

- `secret_key` (str) : The shared secret key. If set, overrides the ``SKA_SECRET_KEY`` variable 
  set in the `settings` module of your project.
- `signature_param` (str): Name of the (for example GET or POST) param name which holds
  the ``signature`` value.
- `auth_user_param` (str): Name of the (for example GET or POST) param name which holds
  the ``auth_user`` value.
- `valid_until_param` (str): Name of the (foe example GET or POST) param name which holds
  the ``valid_until`` value.

If you're using class based views, use the ``m_validate_signed_request`` decorator instead
of ``validate_signed_request``.

Authentication backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Allows you to get a password-less login to Django web site. By default, number of logins using the
same token is not limited. If you wish that single tokens become invalid after first use, set
the following variables to True in your projects' Django settings module.

>>> SKA_DB_STORE_SIGNATURES = True
>>> SKA_DB_PERFORM_SIGNATURE_CHECK = True

Server side
+++++++++++++++++++++++++++++++++++++++++++++++++++
On the server side, where users are supposed to log in, the following shall be present.

settings.py
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
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
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
>>> urlpatterns = patterns('',
>>>     url(r'^ska/', include('ska.contrib.django.ska.urls')),
>>>     url(r'^admin/', include(admin.site.urls)),
>>> )

Callbacks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are several callbacks implemented in authentication backend.

- `USER_GET_CALLBACK` (string): Fired if user was successfully fetched from database (existing user).
- `USER_CREATE_CALLBACK` (string): Fired right after user has been created (user didn't exist).
- `USER_INFO_CALLBACK` (string): Fired upon successful authentication.

Example of a callback function (let's say, it resides in module `my_app.ska_callbacks`):

>>> def my_callback(user, request, signed_request_data)
>>>     # Your code

...where:

- `user` is ``django.contrib.auth.models.User`` instance.
- `request` is ``django.http.HttpRequest`` instance.
- `signed_request_data` is dictionary with signed request data.

For example, if you need to assign user to some local Django group, you could specify the group
name on the client side (add it to the ``extra`` dictionary) and based on that, add the user to
the group in the callback.

The callback is a path qualifier of the callback function. Considering the example above, it would
be "my_app.ska_callbacks.my_callback".

Purging of old signature data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you have lots of visitors and the ``SKA_DB_STORE_SIGNATURES`` set to True, your database
grows. If you wish to get rid of old signature token data, you may want to execute the following
command using a cron job.

    $ ./manage.py ska_purge_stored_signature_data

Client side
+++++++++++++++++++++++++++++++++++++++++++++++++++
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
>>>     extra = {
>>>         'email': 'john.doe@mail.example.com',
>>>         'first_name': 'John',
>>>         'last_name': 'Doe',
>>>     }
>>>     )

Note, that you ``extra`` dictionary is optional! If `email`, `first_name` and `last_name` keys are present,
upon successul validation, the data would be saved into users' profile.

Put this code, for instance, in your view and then make the generated URL available in template context 
and render it as a URL so that user can click on it for authenticating to the server.

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

Multiple secret keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Imagine, you have a site to which you want to offer a password-less login for various clients and
you don't want them all to have one shared secret key, but rather have their own one. Moreover,
you specifically want to execute very custom callbacks not only for each separate client, but
also for different sort of users authenticating.

In order to make the stated above possible, the concept of providers is introduced. You can define
a secret key, callbacks or redirect URL. See an example below.

>>> SKA_PROVIDERS = {
>>>     # Client 1, group users
>>>     'client_1.users': {
>>>         'SECRET_KEY': 'client-1-users-secret-key',
>>>         },
>>>
>>>     # Client 1, group power_users
>>>     'client_1.power_users': {
>>>         'SECRET_KEY': 'client-1-power-users-secret-key',
>>>         'USER_CREATE_CALLBACK': 'foo.ska_callbacks.client1_power_users_create',
>>>         },
>>>
>>>     # Client 1, group admins
>>>     'client_1.admins': {
>>>         'SECRET_KEY': 'client-1-admins-secret-key',
>>>         'USER_CREATE_CALLBACK': 'foo.ska_callbacks.client1_admins_create',
>>>         'REDIRECT_AFTER_LOGIN': '/admin/'
>>>     },
>>> }

See the "Callbacks" section for the list of callbacks.

Obviously, server would have to have the full list of providers defined. On the client side
you would only have to store the general secret key and of course the provider UID(s).

When making a signed URL on the client side, you should be providing the "provider" key in
the ``extra`` argument. See the example below for how you would do it for "client_1.power_users".

>>> from ska import sign_url
>>> from ska.defaults import DEFAULT_PROVIDER_PARAM
>>>
>>> server_ska_login_url = 'https://server-url.com/ska/login/'
>>>
>>> signed_remote_ska_login_url = sign_url(
>>>     auth_user = 'test_ska_user',
>>>     secret_key = 'client-1-power-users-secret-key', # Using provider-specific secret key
>>>     url = server_ska_login_url,
>>>     extra = {
>>>         'email': 'test_ska_user_{0}@mail.example.com'.format(uid),
>>>         'first_name': 'John {0}'.format(uid),
>>>         'last_name': 'Doe {0}'.format(uid),
>>>         DEFAULT_PROVIDER_PARAM: 'client_1.power_users',
>>>     }
>>>     )

License
===================================================
GPL 2.0/LGPL 2.1

Support
===================================================
For any issues contact me at the e-mail given in the `Author` section.

Author
===================================================
Artur Barseghyan <artur.barseghyan@gmail.com>
