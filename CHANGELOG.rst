Release history and notes
=========================
`Sequence based identifiers
<http://en.wikipedia.org/wiki/Software_versioning#Sequence-based_identifiers>`_
are used for versioning (schema follows below):

.. code-block:: none

    major.minor[.revision]

- It's always safe to upgrade within the same minor version (for example, from
  0.3 to 0.3.4).
- Minor version changes might be backwards incompatible. Read the
  release notes carefully before upgrading (for example, when upgrading from
  0.3.4 to 0.4).
- All backwards incompatible changes are mentioned in this document.

1.6.6
-----
2016-12-21

- Minor fixes.

1.6.5
-----
2016-12-06

- Fixed in docs.

1.6.4
-----
2016-12-06

- Added template tags library for Django integration.

1.6.3
-----
2016-12-04

- Fixes in django ska decorators.

1.6.2
-----
2016-12-03

- Fixed broken example installer.

1.6.1
-----
2016-12-03

- Fixes in tests of django-ska package.
- Add shell.py command for easy debugging.
- Minor fixes.
- Clean up docs.

1.6
---
2016-12-02

- Django 1.8, 1.9 and 1.10 compatibility.
- pep8 fixes.
- The ``six`` package requirement increased to six >= 1.9.
- Drop support of Django < 1.8 (it still may work, but no longer guaranteed).
- Drop support of Python 2.6.x.
- Fix broken Django authentication backend, due to deprecation of
  ``request.REQUEST``.

1.5
---
2014-06-04

- Introducing abstract signature class in order to make it possible to define
  more hash algorithms.
- Added HMAC MD5, HMAC SHA-224, HMAC SHA-256, HMAC SHA-384 and HMAC SHA-512
  hash algorythms. HMAC SHA-1 remains a default.

1.4.4
-----
2014-05-06

- Add ``ska-sign-url`` terminal command (Linux only).

1.4.3
-----
2014-02-28

- The ``ValidationResult`` class is slightly changed. The ``reason`` property
  is replaced with ``errors`` (while ``reason`` is left mainly for backwards
  compatibility). For getting human readable message you're encouraged to use
  the ``message`` property (string) instead of joining strings manually.
  Additionally, each error got a separate object (see ``error_codes`` module):
  ``INVALID_SIGNATURE`` and ``SIGNATURE_TIMESTAMP_EXPIRED``.
- Minor documentation improvements.

1.4.2
-----
2013-12-25

- Minor fixes.
- Added authentication backend tests.
- Added tumpering tests.
- Minor documentation improvements.

1.4.1
-----
2013-12-23

- Armenian, Dutch and Russian translations added for Django app.
- Documentation improved.

1.4
---
2013-12-21

- Providers concept implemented. It's now possible to handle multiple secret
  keys and define custom callbacks and redirect URLs per provider. See the
  docs for more.
- Better example project.
- Better documentation.

1.3
---
2013-12-21

- Make it possible to add additional data to the signed request by providing
  an additional ``extra`` argument.
- Reflect the new functionality in Django app.
- Better documentation.

1.2
---
2013-12-17

- Optionally storing the authentication tokens into the database, when used
  with Django auth backend.
- Optionally checking, if signature token has already been used to log into
  Django. If so, ignoring the login attempt. A management command is added to
  purge old signature data.
- Demo (quick installer) added.

1.1
---
2013-12-14

- Class based views validation decorator added.
- Authentication backend for Django based on authentication tokens generated
  with ``ska``.

1.0
---
2013-12-13

- Lowered ``six`` version requirement to 1.1.0.

0.9
---
2013-10-16

- Lowered ``six`` version requirement to 1.4.0.

0.8
---
2013-10-12

- Contrib package ``ska.contrib.django.ska`` added for better Django
  integration.

0.7
---
2013-09-12

- Pinned version requirement of ``six`` package to 1.4.1.

0.6
---
2013-09-06

- Python 2.6.8 and 3.3 support addeded.

0.5
---
2013-09-05

- Stable release.

0.4
---
2013-09-04

- Adding shortcuts for handling dictionaries.
- Improved documentation.

0.3
---
2013-09-04

- Adding commands to generate the URLs.

0.2
---
2013-09-02

- Fixed docs.

0.1
---
2013-09-01

- Initial beta release.
