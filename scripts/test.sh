# ska tests
./uninstall.sh
reset
./install.sh
python src/ska/tests.py

# django-ska tests
python example/example/manage.py migrate --noinput --traceback -v 3
python example/example/manage.py test ska --traceback -v 3
