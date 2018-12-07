#!/usr/bin/env bash
# ska tests
./scripts/uninstall.sh
reset
./scripts/install.sh
python src/ska/tests/__init__.py

# django-ska tests
python examples/simple/manage.py migrate --noinput --traceback -v 3 --settings=settings.testing
python examples/simple/manage.py test ska --traceback -v 3 --settings=settings.testing
