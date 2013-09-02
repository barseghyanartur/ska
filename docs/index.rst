==========================
ska
==========================
Symmetric-key algorithm encryption. Lets you easily generate signatures for signing (HTTP) requests.
Allows you to validate signed requests and identify possible validation errors.

Key concepts
==========================
Host and server share the Secret Key, which is used to sign requests. Secret key is never sent around.

Each HTTP request is signed on the client side using the shared Secret Key and as an outcome produces
the triple (``signature``, ``auth_user``, ``valid_until``) which are used to sign the requests.

- `signature` (str): Signature generated.
- `auth_user` (str): User making the request. Can be anything.
- `valid_until` (float|str): Signature expiration time (Unix timestamp).

On the server side, HTTP request is validated using the shared Secret Key. It's being checked
whether signature is valid and not expired.

Installation
==========================

    $ pip install ska

Usage examples
==========================
Client side
--------------------------
Required imports.

>>> from ska import Signature, RequestHelper

Generate a signature.

>>> signature = Signature.generate_signature(
>>>     auth_user = 'user',
>>>     secret_key = 'your-secret-key'
>>>     )

Create a request helper. Your endpoint operates with certain param names. In order to have the job done
in an easy way, we feed those params to the request helper and let it make a signed endpoint URL for us.

>>> request_helper = RequestHelper(
>>>     signature_param = 'signature',
>>>     auth_user_param = 'auth_user',
>>>     valid_until_param = 'valid_until'
>>> )

Append signature params to the endpoint URL.

>>> url = request_helper.signature_to_url(
>>>     signature = signature,
>>>     endpoint_url = 'http://e.com/api/'
>>> )
http://e.com/api/?valid_until=1378045287.0&auth_user=user&signature=YlZpLFsjUKBalL4x5trhkeEgqE8%3D

Make a request.

>>> import requests
>>> r = requests.get(url)

Server side
--------------------------
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

License
==================================
GPL 2.0/LGPL 2.1

Support
==================================
For any issues contact me at the e-mail given in the `Author` section.

Author
==================================
Artur Barseghyan <artur.barseghyan@gmail.com>

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

