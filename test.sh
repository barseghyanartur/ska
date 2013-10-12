# ska tests
./uninstall.sh
reset
./install.sh
reset
python src/ska/tests.py

# django-ska tests
pip install -r src/ska/contrib/django/ska/requirements.txt
python example/example/manage.py syncdb --noinput --traceback -v 3
python example/example/manage.py test ska --traceback -v 3