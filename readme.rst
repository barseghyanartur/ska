===================================================
ska
===================================================
Symmetric-key algorithm encryption. Lets you easily generate signatures for signing (HTTP) requests.
Allows you to validate signed requests and identify possible validation errors.

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

Installation
===================================================
Latest stable version from PyPi.

    $ pip install ska

Latest stable version from bitbucket.

    $ pip install -e hg+https://bitbucket.org/barseghyanartur/ska@stable#egg=ska

Latest stable version from github.

    $ pip install -e git+https://github.com/barseghyanartur/ska@stable#egg=ska

Usage examples
===================================================
Basic usage
---------------------------------------------------

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
>>> )
{
    'signature': 'YlZpLFsjUKBalL4x5trhkeEgqE8=',
    'auth_user': 'user',
    'valid_until': '1378045287.0'
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

With all customisations, it would look as follows.

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

License
===================================================
GPL 2.0/LGPL 2.1

Support
===================================================
For any issues contact me at the e-mail given in the `Author` section.

Author
===================================================
Artur Barseghyan <artur.barseghyan@gmail.com>
