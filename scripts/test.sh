# ska tests
./uninstall.sh
reset
./install.sh
python src/ska/tests.py

# django-ska tests
python examples/simple/manage.py migrate --noinput --traceback -v 3
python examples/simple/manage.py test ska --traceback -v 3
