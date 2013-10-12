Description
============================
Example project for `django-slim`. It provides good examples of how to build a multi-lingual site using `django-slim`,
and `django-localeurl`.

Installation
============================
1. Install requirements
----------------------------
    $ pip install -r requirements.txt

2. Create database, which will be automatically filled with initial (test) data.
----------------------------
    $ ./manage.py syncdb --noinput

3. Collect static files
----------------------------
    $ ./manage.py collectstatic --noinput

Usage
============================
- Example app comes with initial (test) data installed. Admin credentials are admin:test
- Add some more items and translations to ``FooItem`` model here http://127.0.0.1:8000/admin/foo/fooitem/
- Open http://127.0.0.1:8000/en/foo/ in your browser and navigate through the URLs
