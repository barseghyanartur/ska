# ska tests
./uninstall.sh
reset
./install.sh
pip uninstall six -y
pip uninstall six -y
pip install six==1.1.0
python src/ska/tests.py

# django-ska tests
pip install -r src/ska/contrib/django/ska/requirements.txt
python example/example/manage.py syncdb --noinput --traceback -v 3
python example/example/manage.py test ska --traceback -v 3

pip freeze

pip uninstall six -y
pip uninstall six -y
pip install six==1.4.1
python src/ska/tests.py

# django-ska tests
pip install -r src/ska/contrib/django/ska/requirements.txt
python example/example/manage.py syncdb --noinput --traceback -v 3
python example/example/manage.py test ska --traceback -v 3

pip freeze