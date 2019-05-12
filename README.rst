===
ska
===
Lets you easily sign data, using symmetric-key algorithm encryption. Allows
you to validate signed data and identify possible validation errors. Uses
sha-(1, 224, 256, 385 and 512)/hmac for signature encryption. Allows to use
custom hash algorithms. Comes with shortcut functions for signing (and
validating) dictionaries and URLs.

Key concepts
============
Hosts, that communicate with each other, share the Secret Key, which is used
to sign data (requests). Secret key is never sent around.

One of the cases is signing of HTTP requests. Each (HTTP) request is signed
on the sender side using the shared Secret Key and as an outcome produces the
triple (``signature``, ``auth_user``, ``valid_until``) which are used to sign
the requests.

- ``signature`` (str): Signature generated.
- ``auth_user`` (str): User making the request. Can be anything.
- ``valid_until`` (float|str): Signature expiration time (Unix timestamp).

On the recipient side, (HTTP request) data is validated using the shared
Secret Key. It's being checked whether signature is valid and not expired.

.. code-block:: text

    ┌─────────────┐           Data              ┌─────────────┐
    │   Host 1    ├────────────────────────────>│   Host 2    │
    │ ─────────── │                             │ ─────────── │
    │ secret key  │                             │ secret key  │
    │ 'my-secret' │<────────────────────────────┤ 'my-secret' │
    └─────────────┘           Data              └─────────────┘

Features
========
Core `ska` module
-----------------
- Sign dictionaries.
- Validate signed dictionaries.
- Sign URLs. Append and sign additional URL data.
- Validate URLs.
- Use one of the built-in algorythms (HMAC SHA-1, HMAC SHA-224, HMAC SHA-256,
  HMAC SHA-384 or HMAC SHA-512) or define a custom one.

Django `ska` module (`ska.contrib.django.ska`)
----------------------------------------------
- Model decorators for signing absolute URLs. View (including class-based
  views) decorators for protecting views to authorised parties only (no
  authentication required).
- Authentication backend for Django based on the signatures (tokens) generated
  using `ska`, which allows you to get a password-less login to Django web
  site. Multiple Secret Keys (per provider) supported. Comes with handy
  callbacks (possible to customise per provider) for various states of
  authentication.
- Template tags for signing URLs from within templates.
- `django-constance` integration (for password-less authentication).
- `Django REST Framework integration`_ (for protecting ViewSets, obtaining
  JWT tokens for authentication).

Prerequisites
=============
Present
-------
- Core ``ska`` module requires Python 2.7, 3.5, 3.6 or 3.7.
- Django ``ska`` module (``ska.contrib.django.ska``) requires the mentioned
  above plus Django 1.8, 1.9, 1.10, 1.11, 2.0 or 2.1. Additionally, certain
  versions of `django-constance` and `djangorestframework` are required.
  Specific version requirement primarily depends on the used Django version.
  Check the `example requirements
  <https://github.com/barseghyanartur/ska/tree/master/examples/requirements>`_
  to find out which versions of `django-constance` and `djangorestframework`
  have been tested with specific Django versions.

Past
----
.. note::

    In future releases (any time) compatibility with no-longer-supported
    versions might/will be wiped out.

- Dropping support of Python 3.4 has been announced in version 1.6.8. As of
  1.6.8 everything still worked.
- Dropping support of Django 1.5, 1.6 and 1.7 has been announced in version
  1.6. As of 1.6 everything is still backwards compatible with mentioned
  versions.
- Dropping support of Python 2.6 and 3.3 has been announced in version 1.6.
  As of 1.6 everything is still backwards compatible (as much as it's possible
  within this package) with mentioned versions.

Installation
============
Latest stable version from PyPI:

.. code-block:: sh

    pip install ska

or latest stable version from BitBucket:

.. code-block:: sh

    pip install https://bitbucket.org/barseghyanartur/ska/get/stable.tar.gz

or latest stable version from GitHub.

.. code-block:: sh

    pip install https://github.com/barseghyanartur/ska/archive/stable.tar.gz

Usage examples
==============
For integration with Django, see the `Django integration`_ section.

Basic usage
-----------
Pure Python usage.

Sender side
~~~~~~~~~~~
Signing URLs is as simple as follows.

Required imports.

.. code-block:: python

    from ska import sign_url

Producing a signed URL.

.. code-block:: python

    signed_url = sign_url(
        auth_user='user',
        secret_key='your-secret_key',
        url='http://e.com/api/'
    )

.. code-block:: text

    GET http://e.com/api/?valid_until=1378045287.0&auth_user=user&signature=YlZpLFsjUKBalL4x5trhkeEgqE8%3D

Default lifetime of a signature is 10 minutes (600 seconds). If you want it
to be different, provide a ``lifetime`` argument to ``sign_url`` function.

Default name of the (GET) param holding the generated signature value
is ``signature``. If you want it to be different, provide a ``signature_param``
argument to ``sign_url`` function.

Default name of the (GET) param holding the ``auth_user`` value is
``auth_user``. If you want it to be different, provide a ``auth_user_param``
argument to ``sign_url`` function.

Default name of the (GET) param holding the ``valid_until`` value is
`valid_until`. If you want it to be different, provide a ``valid_until_param``
argument to ``sign_url`` function.

Note, that by default a suffix '?' is added after the given ``url`` and
generated signature params. If you want that suffix to be custom, provide a
``suffix`` argument to the ``sign_url`` function. If you want it to be gone,
set its' value to empty string.

With all customisations, it would look as follows:

.. code-block:: python

    from ska import HMACSHA512Signature  # Use HMAC SHA-512 algorithm

    signed_url = sign_url(
        auth_user='user',
        secret_key='your-secret_key',
        lifetime=120,
        url='http://e.com/api/',
        signature_param='signature',
        auth_user_param='auth_user',
        valid_until_param='valid_until',
        signature_cls=HMACSHA512Signature
    )

It's also possible to add additional data to the signature by providing a
``extra`` argument (dict). Note, that additional data is signed as well.
If request is somehow tampered (values vary from originally provided ones),
signature becomes invalid.

.. code-block:: python

    sign_url(
        auth_user='user',
        secret_key='your-secret_key',
        url='http://e.com/api/',
        extra={
            'email': 'doe@example.com',
            'last_name': 'Doe',
            'first_name': 'Joe'
        }
    )

You may now proceed with the signed URL request. If you use the famous
``requests`` library, it would be as follows.

.. code-block:: python

    import requests
    requests.get(signed_url)

If you want to use POST method instead, you would likely want to get a
dictionary back, in order to append it to the POST data later.

Required imports.

.. code-block:: python

    from ska import signature_to_dict

Producing a dictionary containing the signature data, ready to be put into
the request (for example POST) data. All customisations mentioned above for
the ``sign_url`` function, also apply to the ``signature_to_dict``:

.. code-block:: python

    signature_dict = signature_to_dict(
        auth_user='user',
        secret_key='your-secret_key'
    )

.. code-block:: text

    {
        'signature': 'YlZpLFsjUKBalL4x5trhkeEgqE8=',
        'auth_user': 'user',
        'valid_until': '1378045287.0'
    }

Adding of additional data to the signature works in the same way:

.. code-block:: python

    signature_dict = signature_to_dict(
        auth_user='user',
        secret_key='your-secret_key',
        extra={
            'email': 'john.doe@mail.example.com',
            'first_name': 'John',
            'last_name': 'Doe'
        }
    )

.. code-block:: text

    {
        'auth_user': 'user',
        'email': 'john.doe@mail.example.com',
        'extra': 'email,first_name,last_name',
        'first_name': 'John',
        'last_name': 'Doe',
        'signature': 'cnSoU/LnJ/ZhfLtDLzab3a3gkug=',
        'valid_until': 1387616469.0
    }

If you for some reason prefer a lower level implementation, read the same
section in the `Advanced usage (low-level)`_ chapter.

Recipient side
~~~~~~~~~~~~~~
Validating the signed request data is as simple as follows.

Required imports.

.. code-block:: python

    from ska import validate_signed_request_data

Validating the signed request data. Note, that ``data`` value is expected to
be a dictionary; ``request.GET`` is given as an example. It will most likely
vary from what's used in your framework (unless you use Django).

.. code-block:: python

    validation_result = validate_signed_request_data(
        data=request.GET,  # Note, that ``request.GET`` is given as example.
        secret_key='your-secret_key'
    )

The ``validate_signed_request_data`` produces a
``ska.SignatureValidationResult`` object, which holds the following data.

- ``result`` (bool): True if data is valid. False otherwise.
- ``reason`` (list): List of strings, indicating validation errors. Empty list
  in case if ``result`` is True.

Default name of the (GET) param holding the signature value is `signature`.
If you want it to be different, provide a ``signature_param`` argument to
``validate_signed_request_data`` function.

Default name of the (GET) param holding the ``auth_user`` value is
``auth_user``. If you want it to be different, provide a ``auth_user_param``
argument to ``validate_signed_request_data`` function.

Default name of the (GET) param holding the ``valid_until`` value is
``valid_until``. If you want it to be different, provide a
``valid_until_param`` argument to ``validate_signed_request_data`` function.

With all customisations, it would look as follows. Note, that
``request.GET`` is given as example.

.. code-block:: python

    from ska import HMACSHA256Signature  # Use HMAC SHA-256 algorithm

    validation_result = validate_signed_request_data(
        data=request.GET,
        secret_key='your-secret_key',
        signature_param='signature',
        auth_user_param='auth_user',
        valid_until_param='valid_until',
        signature_cls=HMACSHA256Signature
    )

If you for some reason prefer a lower level implementation, read the same
section in the `Advanced usage (low-level)`_ chapter.

Command line usage
------------------
It's possible to generate a signed URL from command line using the
``ska.generate_signed_url`` module.

:Arguments:

.. code-block:: text

    -h, --help            show this help message and exit

    -au AUTH_USER, --auth-user AUTH_USER
                          `auth_user` value

    -sk SECRET_KEY, --secret-key SECRET_KEY
                          `secret_key` value

    -vu VALID_UNTIL, --valid-until VALID_UNTIL
                          `valid_until` value

    -l LIFETIME, --lifetime LIFETIME
                          `lifetime` value

    -u URL, --url URL     URL to sign

    -sp SIGNATURE_PARAM, --signature-param SIGNATURE_PARAM
                          (GET) param holding the `signature` value

    -aup AUTH_USER_PARAM, --auth-user-param AUTH_USER_PARAM
                          (GET) param holding the `auth_user` value

    -vup VALID_UNTIL_PARAM, --valid-until-param VALID_UNTIL_PARAM
                          (GET) param holding the `auth_user` value

:Example:

.. code-block:: sh

    ska-sign-url -au user -sk your-secret-key --url http://example.com

Advanced usage (low-level)
--------------------------
Sender side
~~~~~~~~~~~

Required imports.

.. code-block:: python

    from ska import Signature, RequestHelper

Generate a signature.

.. code-block:: python

    signature = Signature.generate_signature(
        auth_user='user',
        secret_key='your-secret-key'
    )

Default lifetime of a signature is 10 minutes (600 seconds). If you want it to
be different, provide a ``lifetime`` argument to ``generate_signature``
method.

.. code-block:: python

    signature = Signature.generate_signature(
        auth_user='user',
        secret_key='your-secret-key',
        lifetime=120  # Signatre lifetime set to 120 seconds.
    )

Adding of additional data to the signature works in the same way as in
``sign_url``.

.. code-block:: python

    signature = Signature.generate_signature(
        auth_user='user',
        secret_key='your-secret-key',
        extra={
            'email': 'doe@example.com',
            'last_name': 'Doe',
            'first_name': 'Joe'
        }
    )

For HMAC SHA-384 algorithm it would look as follows.

.. code-block:: python

    from ska import HMACSHA384Signature

    signature = HMACSHA384Signature.generate_signature(
        auth_user='user',
        secret_key='your-secret-key'
    )

Your endpoint operates with certain param names and you need to wrap generated
signature params into the URL. In order to have the job done in an easy way,
create a request helper. Feed names of the (GET) params to the request helper
and let it make a signed endpoint URL for you.

.. code-block:: python

    request_helper = RequestHelper(
        signature_param='signature',
        auth_user_param='auth_user',
        valid_until_param='valid_until'
    )

Append signature params to the endpoint URL.

.. code-block:: python

    signed_url = request_helper.signature_to_url(
        signature=signature,
        endpoint_url='http://e.com/api/'
    )

.. code-block:: text

    GET http://e.com/api/?valid_until=1378045287.0&auth_user=user&signature=YlZpLFsjUKBalL4x5trhkeEgqE8%3D

Make a request.

.. code-block:: python

    import requests
    r = requests.get(signed_url)


For HMAC SHA-384 algorithm it would look as follows.

.. code-block:: python

    from ska import HMACSHA384Signature

    request_helper = RequestHelper(
        signature_param='signature',
        auth_user_param='auth_user',
        valid_until_param='valid_until',
        signature_cls=HMACSHA384Signature
    )

    signed_url = request_helper.signature_to_url(
        signature=signature,
        endpoint_url='http://e.com/api/'
    )

Recipient side
~~~~~~~~~~~~~~
Required imports.

.. code-block:: python

    from ska import RequestHelper

Create a request helper. Your endpoint operates with certain param names. In
order to have the job done in an easy way, we feed those params to the
request helper and let it extract data from signed request for us.

.. code-block:: python

    request_helper = RequestHelper(
        signature_param='signature',
        auth_user_param='auth_user',
        valid_until_param='valid_until'
    )

Validate the request data. Note, that ``request.GET`` is given just as an
example.

.. code-block:: python

    validation_result = request_helper.validate_request_data(
        data=request.GET,
        secret_key='your-secret-key'
    )

Your implementation further depends on you, but may look as follows.

.. code-block:: python

    if validation_result.result:
        # Validated, proceed further
        # ...
    else:
        # Validation not passed.
        raise Http404(validation_result.reason)

You can also just validate the signature by calling ``validate_signature``
method of the ``ska.Signature``.

.. code-block:: python

    Signature.validate_signature(
        signature='EBS6ipiqRLa6TY5vxIvZU30FpnM=',
        auth_user='user',
        secret_key='your-secret-key',
        valid_until='1377997396.0'
    )

Django integration
------------------
``ska`` comes with Django model- and view-decorators for producing signed URLs
and and validating the endpoints, as well as with authentication backend,
which allows password-less login into Django web site using `ska` generated
signature tokens. There's also a template tag for signing URLs.

Demo
~~~~
In order to be able to quickly evaluate the ``ska``, a demo app (with a quick
installer) has been created (works on Ubuntu/Debian, may work on other Linux
systems as well, although not guaranteed). Follow the instructions below for
having the demo running within a minute.

Grab the latest ``ska_example_app_installer.sh`` and execute it:

.. code-block:: sh

    wget -O - https://raw.github.com/barseghyanartur/ska/stable/examples/ska_example_app_installer.sh | bash

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
~~~~~~~~~~~~~
Secret key (str) must be defined in `settings` module of your project.

.. code-block:: python

    SKA_SECRET_KEY = 'my-secret-key'

The following variables can be overridden in ``settings`` module of your
project.

- ``SKA_UNAUTHORISED_REQUEST_ERROR_MESSAGE`` (str): Plain text error message.
  Defaults to "Unauthorised request. {0}".
- ``SKA_UNAUTHORISED_REQUEST_ERROR_TEMPLATE`` (str): Path to 401 template that
  should be rendered in case of 401
  responses. Defaults to empty string (not provided).
- ``SKA_AUTH_USER`` (str): The ``auth_user`` argument for ``ska.sign_url``
  function. Defaults to "ska-auth-user".

See the working `example project
<https://github.com/barseghyanartur/ska/tree/stable/example>`_.

Multiple secret keys
~~~~~~~~~~~~~~~~~~~~
Imagine, you have a site to which you want to offer a password-less login for
various clients/senders and you don't want them all to have one shared secret
key, but rather have their own one. Moreover, you specifically want to execute
very custom callbacks not only for each separate client/sender, but also for
different sort of users authenticating.

.. code-block:: text

                              ┌────────────────┐
                              │ Site providing │
                              │ authentication │
                              │ ────────────── │
                              │ custom secret  │
                              │    keys per    │
                              │     client     │
                              │ ────────────── │
                              │ Site 1: 'sk-1' │
                 ┌───────────>│ Site 2: 'sk-2' │<───────────┐
                 │            │ Site 3: 'sk-3' │            │
                 │      ┌────>│ Site 4: 'sk-4' │<────┐      │
                 │      │     └────────────────┘     │      │
                 │      │                            │      │
                 │      │                            │      │
    ┌────────────┴─┐  ┌─┴────────────┐  ┌────────────┴─┐  ┌─┴────────────┐
    │    Site 1    │  │    Site 2    │  │    Site 3    │  │    Site 4    │
    │ ──────────── │  │ ──────────── │  │ ──────────── │  │ ──────────── │
    │  secret key  │  │  secret key  │  │  secret key  │  │  secret key  │
    │    'sk-1'    │  │    'sk-2'    │  │    'sk-3'    │  │    'sk-4'    │
    └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘

In order to make the stated above possible, the concept of providers is
introduced. You can define a secret key, callbacks or redirect URL. See an
example below. Note, that keys of the ``SKA_PROVIDERS`` ("client_1",
"client_2", etc.) are the provider keys.

.. code-block:: python

    SKA_PROVIDERS = {
        # ********************************************************
        # ******************** Basic gradation *******************
        # ********************************************************
        # Site 1
        'client_1': {
            'SECRET_KEY': 'sk-1',
        },

        # Site 2
        'client_2': {
            'SECRET_KEY': 'sk-2',
        },

        # Site 3
        'client_3': {
            'SECRET_KEY': 'sk-3',
        },

        # Site 4
        'client_4': {
            'SECRET_KEY': 'sk-4',
        },

        # ********************************************************
        # ******* You make gradation as complex as you wish ******
        # ********************************************************
        # Client 1, group users
        'client_1.users': {
            'SECRET_KEY': 'client-1-users-secret-key',
        },

        # Client 1, group power_users
        'client_1.power_users': {
            'SECRET_KEY': 'client-1-power-users-secret-key',
            'USER_CREATE_CALLBACK': 'foo.ska_callbacks.client1_power_users_create',
        },

        # Client 1, group admins
        'client_1.admins': {
            'SECRET_KEY': 'client-1-admins-secret-key',
            'USER_CREATE_CALLBACK': 'foo.ska_callbacks.client1_admins_create',
            'REDIRECT_AFTER_LOGIN': '/admin/'
        },
    }

See the `Callbacks`_ section for the list of callbacks. Note, that callbacks
defined in the ``SKA_PROVIDERS`` are overrides. If a certain callback isn't
defined in the ``SKA_PROVIDERS``, authentication backend falls back to the
respective default callback function.

Obviously, server would have to have the full list of providers defined. On
the client side you would only have to store the general secret key and of
course the provider UID(s).

When making a signed URL on the sender side, you should be providing the
``provider`` key in the ``extra`` argument. See the example below for how you
would do it for ``client_1.power_users``.

.. code-block:: python

    from ska import sign_url
    from ska.defaults import DEFAULT_PROVIDER_PARAM

    server_ska_login_url = 'https://server-url.com/ska/login/'

    signed_remote_ska_login_url = sign_url(
        auth_user='test_ska_user',
        # Using provider-specific secret key. This value shall be equal to
        # the value of SKA_PROVIDERS['client_1.power_users']['SECRET_KEY'],
        # defined in your projects' Django settings module.
        secret_key='client-1-power-users-secret-key',
        url=server_ska_login_url,
        extra={
            'email': 'test_ska_user@mail.example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            # Using provider specific string. This value shall be equal to
            # the key string "client_1.power_users" of SKA_PROVIDERS,
            # defined in your projcts' Django settings module.
            DEFAULT_PROVIDER_PARAM: 'client_1.power_users',
        }
    )

Django model method decorator ``sign_url``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This is most likely be used in module ``models`` (models.py).

Imagine, you have a some objects listing and you want to protect the URLs to
be viewed by authorised parties only. You would then use
``get_signed_absolute_url`` method when rendering the listing (HTML).

.. code-block:: python

    from django.db import models
    from django.utils.translation import ugettext_lazy as _
    from django.core.urlresolvers import reverse

    from ska.contrib.django.ska.decorators import sign_url


    class FooItem(models.Model):

        title = models.CharField(_("Title"), max_length=100)
        slug = models.SlugField(unique=True, verbose_name=_("Slug"))
        body = models.TextField(_("Body"))

        # Unsigned absolute URL, which goes to the foo item detail page.
        def get_absolute_url(self):
            return reverse('foo.detail', kwargs={'slug': self.slug})

        # Signed absolute URL, which goes to the foo item detail page.
        @sign_url()
        def get_signed_absolute_url(self):
            return reverse('foo.detail', kwargs={'slug': self.slug})

Note, that ``sign_url`` decorator accepts the following optional arguments.

- ``auth_user`` (str): Username of the user making the request.
- ``secret_key``: The shared secret key. If set, overrides
  the ``SKA_SECRET_KEY`` variable set in the `settings` module of your
  project.
- ``valid_until`` (float or str ): Unix timestamp. If not given, generated
  automatically (now + lifetime).
- ``lifetime`` (int): Signature lifetime in seconds.
- ``suffix`` (str): Suffix to add after the ``endpoint_url`` and before the
  appended signature params.
- ``signature_param`` (str): Name of the GET param name which would hold the
  generated signature value.
- `auth_user_param` (str): Name of the GET param name which would hold
  the ``auth_user`` value.
- ``valid_until_param`` (str): Name of the GET param name which would hold
  the ``valid_until`` value.

Django view decorator ``validate_signed_request``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To be used to protect views (file views.py). Should be applied to
views (endpoints) that require signed requests. If checks are not successful,
a ``ska.contrib.django.ska.http.HttpResponseUnauthorized`` is returned, which
is a subclass of Django's ``django.http.HttpResponse``. You can provide your
own template for 401 error. Simply point the
``SKA_UNAUTHORISED_REQUEST_ERROR_TEMPLATE`` in `settings` module to the right
template. See ``ska/contrib/django/ska/templates/ska/401.html`` as a template
example.

.. code-block:: python

    from ska.contrib.django.ska.decorators import validate_signed_request

    # Your view that shall be protected
    @validate_signed_request()
    def detail(request, slug, template_name='foo/detail.html'):
        # Your code

Note, that ``validate_signed_request`` decorator accepts the following optional
arguments.

- ``secret_key`` (str) : The shared secret key. If set, overrides
  the ``SKA_SECRET_KEY`` variable  set in the ``settings`` module of your
  project.
- ``signature_param`` (str): Name of the (for example GET or POST) param name
  which holds the ``signature`` value.
- ``auth_user_param`` (str): Name of the (for example GET or POST) param name
  which holds the ``auth_user`` value.
- ``valid_until_param`` (str): Name of the (foe example GET or POST) param
  name which holds the ``valid_until`` value.

If you're using class based views, use the ``m_validate_signed_request``
decorator instead of ``validate_signed_request``.

Template tags
~~~~~~~~~~~~~
There are two template tags modules: ``ska_tags`` and ``ska_constance_tags``.
They are functionally identical, although ``ska_constance_tags`` is tied to
``django-constance``.

For standard settings configurations, template tags shall be loaded as follows:

.. code-block:: html

    {% load ska_tags %}

For ``django-constance`` based settings configurations, template tags shall be
loaded as follows:

.. code-block:: html

    {% load ska_constance_tags %}

sign_url
++++++++
The ``sign_url`` template tag accepts template context and the following
params:

- url
- auth_user: If not given, request.user.get_username() is used.
- secret_key: If not given, the secret key from settings is used.
- valid_until: If not given, calculated from ``lifetime``.
- lifetime: Defaults to ``ska.defaults.SIGNATURE_LIFETIME``.
- suffix: Defaults to ``ska.defaults.DEFAULT_URL_SUFFIX``.
- signature_param: Defaults to ``ska.defaultsDEFAULT_SIGNATURE_PARAM``.
- auth_user_param: Defaults to ``ska.defaults.DEFAULT_AUTH_USER_PARAM``.
- valid_until_param: Defaults to ``ska.defaults.DEFAULT_VALID_UNTIL_PARAM``.
- signature_cls: Defaults to ``ska.signatures.Signature``.

Usage example:

.. code-block:: html

    {% load ska_tags %}

    {% for item in items%}

        {% sign_url item.get_absolute_url as item_signed_absolute_url %}
        <a href="{{ item_signed_absolute_url }}">{{ item }}</a>

    {% endfor %}

provider_sign_url
+++++++++++++++++
The ``provider_sign_url`` template tag accepts template context and the
following params:

- url
- provider: Provider name.
- auth_user: If not given, request.user.get_username() is used.
- valid_until: If not given, calculated from ``lifetime``.
- lifetime: Defaults to ``ska.defaults.SIGNATURE_LIFETIME``.
- suffix: Defaults to ``ska.defaults.DEFAULT_URL_SUFFIX``.
- signature_param: Defaults to ``ska.defaultsDEFAULT_SIGNATURE_PARAM``.
- auth_user_param: Defaults to ``ska.defaults.DEFAULT_AUTH_USER_PARAM``.
- valid_until_param: Defaults to ``ska.defaults.DEFAULT_VALID_UNTIL_PARAM``.
- signature_cls: Defaults to ``ska.signatures.Signature``.
- fail_silently: Defaults to False.

Usage example:

.. code-block:: html

    {% load ska_tags %}

    {% for item in items%}

        {% provider_sign_url url=item.get_absolute_url provider='client_1.users' as item_signed_absolute_url %}
        <a href="{{ item_signed_absolute_url }}">{{ item }}</a>

    {% endfor %}

Authentication backends
~~~~~~~~~~~~~~~~~~~~~~~
Allows you to get a password-less login to Django web site.

At the moment there are two backends implemented:

- `SkaAuthenticationBackend`_: Uses standard Django settings.
- `SkaAuthenticationConstanceBackend`_: Relies on dynamic settings
  functionality provided by `django-constance`.

By default, number of logins using the same token is not limited. If you wish
that single tokens become invalid after first use, set the following variables
to True in your projects' Django settings module.

.. code-block:: python

    SKA_DB_STORE_SIGNATURES = True
    SKA_DB_PERFORM_SIGNATURE_CHECK = True

SkaAuthenticationBackend
++++++++++++++++++++++++
``SkaAuthenticationBackend`` uses standard Django settings.

Recipient side
^^^^^^^^^^^^^^
Recipient is the host (Django site), to which the sender tries to get
authenticated (log in). On the recipient side the following shall be present.

settings.py
***********
.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        'ska.contrib.django.ska.backends.SkaAuthenticationBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    INSTALLED_APPS = (
        # ...
        'ska.contrib.django.ska',
        # ...
    )

    SKA_SECRET_KEY = 'secret-key'
    SKA_UNAUTHORISED_REQUEST_ERROR_TEMPLATE = 'ska/401.html'
    SKA_REDIRECT_AFTER_LOGIN = '/foo/logged-in/'

urls.py
*******
.. code-block:: python

    urlpatterns = [
        url(r'^ska/', include('ska.contrib.django.ska.urls')),
        url(r'^admin/', include(admin.site.urls)),
    ]

Callbacks
*********
There are several callbacks implemented for authentication backend.

- ``USER_VALIDATE_CALLBACK`` (string): Validate request callback. Created to
  allow adding custom logic to the incoming authentication requests. The main
  purpose is to provide a flexible way of raising exceptions if the incoming
  authentication request shall be blocked (for instance, email or username is
  in black-list or right the opposite - not in the white list). The only aim of
  the `USER_VALIDATE_CALLBACK` is to raise a ``django.core.PermissionDenied``
  exception if request data is invalid. In that case authentication flow will
  halt. All other exceptions would simply be ignored (but logged) and if no
  exception raised, the normal flow would be continued.
- ``USER_GET_CALLBACK`` (string): Fired if user was successfully fetched from
  database (existing user).
- ``USER_CREATE_CALLBACK`` (string): Fired right after user has been
  created (user didn't exist).
- ``USER_INFO_CALLBACK`` (string): Fired upon successful authentication.

Example of a callback function (let's say, it resides in module
``my_app.ska_callbacks``):

.. code-block:: python

    def my_callback(user, request, signed_request_data)
        # Your code

...where:

- ``user`` is ``django.contrib.auth.models.User`` instance.
- ``request`` is ``django.http.HttpRequest`` instance.
- ``signed_request_data`` is dictionary with signed request data.

For example, if you need to assign user to some local Django group, you could
specify the group name on the client side (add it to the ``extra`` dictionary)
and based on that, add the user to the group in the callback.

The callback is a path qualifier of the callback function. Considering the
example above, it would be ``my_app.ska_callbacks.my_callback``.

Prefix names of each callback variable with `SKA_` in your projects' settings
module.

Example:

.. code-block:: python

    SKA_USER_GET_CALLBACK = 'my_app.ska_callbacks.my_get_callback'
    SKA_USER_CREATE_CALLBACK = 'my_app.ska_callbacks.my_create_callback'

Sender side
^^^^^^^^^^^
Sender is the host (another Django web site) from which users authenticate to
the Recipient using signed URLs.

On the sender side, the only thing necessary to be present is the ``ska``
module for Django and of course the same ``SECRET_KEY`` as on the server side.
Further, the server ``ska`` login URL (in our case "/ska/login/") shall be
signed using ``ska`` (for example, using ``sign_url`` function). The
``auth_user`` param would be used as a Django username. See the example below.

.. code-block:: python

    from ska import sign_url
    from ska.contrib.django.ska.settings import SECRET_KEY

    server_ska_login_url = 'https://server-url.com/ska/login/'

    signed_url = sign_url(
        auth_user='test_ska_user_0',
        secret_key=SECRET_KEY,
        url=server_ska_login_url,
        extra={
            'email': 'john.doe@mail.example.com',
            'first_name': 'John',
            'last_name': 'Doe',
        }
    )

Note, that you ``extra`` dictionary is optional! If ``email``, ``first_name``
and ``last_name`` keys are present, upon successful validation, the data
would be saved into users' profile.

Put this code, for instance, in your view and then make the generated URL
available in template context and render it as a URL so that user can click
on it for authenticating to the server.

.. code-block:: python

    def auth_to_server(request, template_name='auth_to_server.html'):
        # Some code + obtaining the `signed_url` (code shown above)
        context = {'signed_url': signed_url}

        return render(request, template_name, context)

SkaAuthenticationConstanceBackend
+++++++++++++++++++++++++++++++++
Relies on dynamic settings functionality provided by
`django-constance <https://django-constance.readthedocs.io>`_.

*Only differences with `SkaAuthenticationBackend` are mentioned.*

.. note::

    Additional requirements shall be installed. See the `constance.txt
    <https://github.com/barseghyanartur/ska/blob/master/examples/requirements/constance.txt>`_
    file for additional requirements (``django-constance``,
    ``django-json-widget``, ``django-picklefield``, ``jsonfield2`` and
    ``redis``).

settings.py
^^^^^^^^^^^

.. code-block:: python

    AUTHENTICATION_BACKENDS = (
        'ska.contrib.django.ska.backends.SkaAuthenticationConstanceBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    INSTALLED_APPS = (
        # ...
        'constance',  # django-constance
        'ska.contrib.django.ska',
        'django_json_widget',  # For nice admin JSON widget
        # ...
    )

    CONSTANCE_CONFIG = {
        'SKA_PROVIDERS': (
            {},  # The default value
            'JSON data',  # Help text in admin
            'JSONField_config',  # Field config
        )
    }

    CONSTANCE_ADDITIONAL_FIELDS = {
        'JSONField_config': [
            # `jsonfield2` package might be used for storing the JSON field,
            # however, at the moment of writing it has a bug which makes
            # the JSON invalid after the first save. To avoid that, it has
            # been patched and resides in examples/simple/jsonfield2_addons/
            # module.
            'jsonfield2_addons.forms.JSONField',
            {
                'widget': 'django_json_widget.widgets.JSONEditorWidget',
            }
        ],
    }

    CONSTANCE_BACKEND = 'constance.backends.redisd.RedisBackend'

    CONSTANCE_REDIS_CONNECTION = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }

.. note::

    In very tiny bits, although not required, the
    `jsonfield2 <https://pypi.org/project/jsonfield2/>`_ and
    `django-json-widget <https://pypi.org/project/django-json-widget/>`_
    packages are used for editing of the ``SKA_PROVIDERS`` setting in Django
    admin.

.. note::

    In the example shown above, the ``RedisBackend`` of ``django-constance``
    is used. You could also use ``DatabaseBackend``. Study the
    `documentation <https://django-constance.readthedocs.io/en/latest/backends.html>`_
    for more.

.. note::

    If your `SKA_PROVIDERS` settings are stored in the constance as ``str``
    instead of ``dict``, set the setting
    ``SKA_CONSTANCE_SETTINGS_PARSE_FROM_JSON`` to ``True``.

With ``DatabaseBackend`` it would look as follows:

.. code-block:: python

    CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

    INSTALLED_APPS = (
        # ...
        'constance.backends.database',
        # ...
    )

**Quick demo of the dynamic backend**

- Clone this project:

.. code-block:: sh

    git clone git@github.com:barseghyanartur/ska.git

- Install/migrate:

.. code-block:: sh

    ./scripts/install.sh
    pip install -r examples/requirements/django_2_1.txt
    ./scripts/migrate.sh --settings=settings.constance_settings

- Run:

.. code-block:: sh

    ./scripts/runserver.sh --settings=settings.constance_settings

- Go to `http://localhost:8000/admin/constance/config/
  <http://localhost:8000/admin/constance/config/>`_.

- Paste the following code:

.. code-block:: javascript

    {
       "client_1.users":{
          "SECRET_KEY":"client-1-users-secret-key"
       },
       "client_1.power_users":{
          "SECRET_KEY":"client-1-power-users-secret-key",
          "USER_CREATE_CALLBACK":"foo.ska_callbacks.client1_power_users_create"
       },
       "client_1.admins":{
          "SECRET_KEY":"client-1-admins-secret-key",
          "USER_CREATE_CALLBACK":"foo.ska_callbacks.client1_admins_create",
          "USER_GET_CALLBACK":"foo.ska_callbacks.client1_admins_get",
          "USER_INFO_CALLBACK":"foo.ska_callbacks.client1_admins_info_constance",
          "REDIRECT_AFTER_LOGIN":"/admin/auth/user/"
       }
    }

- Open `http://localhost:8000/foo/authenticate/
  <http://localhost:8000/foo/authenticate/>`_ in another browser and navigate
  to the ``Log in - client_1.admins`` link in the ``Success`` table column of
  the ``By provider`` section. Upon clicking, you should be logged in.
  You have used the dynamic settings.

urls.py
^^^^^^^
``django-constance`` specific views and urls are used. See
`ska.contrib.django.ska.views.constance_views
<https://github.com/barseghyanartur/ska/blob/master/src/ska/contrib/django/ska/views/constance_views.py>`_
and `ska.contrib.django.ska.urls.constance_urls
<https://github.com/barseghyanartur/ska/blob/master/src/ska/contrib/django/ska/urls/constance_urls.py>`_
for the reference.

.. code-block:: python

    urlpatterns = [
        url(r'^ska/', include('ska.contrib.django.ska.urls.constance_urls')),
        url(r'^admin/', include(admin.site.urls)),
    ]

Custom authentication backend
+++++++++++++++++++++++++++++
To implement alternative authentication backend, see the following example:

.. code-block:: python

    from constance import config

    from ska.contrib.django.backends import BaseSkaAuthenticationBackend

    class SkaAuthenticationConstanceBackend(BaseSkaAuthenticationBackend):
        """Authentication backend."""

        def get_settings(self):
            """

            :return:
            """
            return config.SKA_PROVIDERS

That's it. The only thing the ``get_settings`` method shall return is ``dict``
with providers data (see the `Multiple secret keys`_ for the reference;
return value of the ``get_settings` is ``SKA_PROVIDERS`` dict).

Purging of old signature data
+++++++++++++++++++++++++++++
If you have lots of visitors and the ``SKA_DB_STORE_SIGNATURES`` set to True,
your database grows. If you wish to get rid of old signature token data, you
may want to execute the following command using a cron job.

.. code-block:: sh

    ./manage.py ska_purge_stored_signature_data

Security notes
++++++++++++++
From point of security, you should be serving the following pages via HTTP
secure connection:

- The server login page (/ska/login/).
- The client page containing the authentication links.

Django REST Framework integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Permission classes
++++++++++++++++++
For protecting views without actually being authenticated into the system,
specific permission classes are implemented (for both plan settings and
provider settings, as well as both plain- and provider-settings work in
combination with `django-constance` package).

The following permission classes are implemented:

- SignedRequestRequired
- ProviderSignedRequestRequired
- ConstanceSignedRequestRequired
- ConstanceProviderSignedRequestRequired

**ProviderSignedRequestRequired example**

.. code-block:: python

    from rest_framework.viewsets import ModelViewSet

    from ska.contrib.django.ska.integration.drf.permissions import (
        ProviderSignedRequestRequired
    )

    from .models import FooItem
    from .serializers import FooItemSerializer

    class FooItemViewSet(ModelViewSet):
        """FooItem model viewset."""

        permission_classes = (ProviderSignedRequestRequired,)
        queryset = FooItem.objects.all()
        serializer_class = FooItemSerializer

**Signing requests**

Requests are signed the same way. Sample code:

.. code-block:: python

    # Given that we have `auth_user`, `auth_user_email`, `provider_name`
    # (and the rest), the code would look as follows:

    from ska import sign_url
    from ska.defaults import DEFAULT_PROVIDER_PARAM

    extra = {
        'email': auth_user_email,
        'first_name': first_name,
        'last_name': last_name,
    }

    if provider_name:
        extra.update({DEFAULT_PROVIDER_PARAM: provider_name})

    signed_url = sign_url(
        auth_user=auth_user,
        secret_key=secret_key,
        url=url,
        extra=extra
    )

JWT tokens for authentication
+++++++++++++++++++++++++++++
For obtaining JWT tokens for authentication. Also works with
`django-constance`.

**settings example**

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework.authentication.BasicAuthentication',
        ),
    }

**urls example**

.. code-block:: python

    urlpatterns = [
        # ...
        url(
            r'^ska-rest/',
            include('ska.contrib.django.ska.integration.drf.urls.jwt_token')
        ),
    ]

**Sample request**

.. code-block:: text

    http://localhost:8008/ska-rest/obtain-jwt-token/
        ?signature=P92KWDDe0U84Alvu0tvmYoi8e8s%3D
        &auth_user=test_ska_user
        &valid_until=1548195246.0
        &extra=email%2Cfirst_name%2Clast_name
        &email=test_ska_user%40mail.example.com
        &first_name=John
        &last_name=Doe

**Sample response**

.. code-block:: text

    HTTP 200 OK
    Allow: GET, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

.. code-block:: javascript

    {
        "token": "eyJ0eXAiO.eyJ1c2VyX2lkIjo.m_saOvyKBO3"
    }

Testing
=======
Simply type:

.. code-block:: sh

    ./runtests.py

Or use tox:

.. code-block:: sh

    tox

Or use tox to check specific env:

.. code-block:: sh

    tox -e py35

Or run Django tests:

.. code-block:: sh

    python examples/simple/manage.py test ska --settings=settings.testing

Writing documentation
=====================
Keep the following hierarchy.

.. code-block:: text

    =====
    title
    =====

    header
    ======

    sub-header
    ----------

    sub-sub-header
    ~~~~~~~~~~~~~~

    sub-sub-sub-header
    ++++++++++++++++++

    sub-sub-sub-sub-header
    ^^^^^^^^^^^^^^^^^^^^^^

    sub-sub-sub-sub-sub-header
    **************************

License
=======
GPL 2.0/LGPL 2.1

Support
=======
For any issues contact me at the e-mail given in the `Author`_ section.

Author
======
Artur Barseghyan <artur.barseghyan@gmail.com>
