wget -O ska_example_app_installer.tar.gz https://github.com/barseghyanartur/ska/archive/stable.tar.gz
virtualenv ska
source ska/bin/activate
mkdir ska_example_app_installer/
tar -xvf ska_example_app_installer.tar.gz -C ska_example_app_installer
cd ska_example_app_installer/ska-stable/examples/simple/
#cd ska_example_app_installer/ska-master/examples/simple/
pip install -r ../../src/ska/contrib/django/ska/requirements.txt
pip install https://github.com/barseghyanartur/ska/archive/stable.tar.gz
mkdir ../media/
mkdir ../media/static/
mkdir ../static/
mkdir ../db/
mkdir ../logs/
mkdir ../tmp/
cp settings/local_settings.example settings/local_settings.py
./manage.py syncdb --noinput --traceback -v 3
./manage.py migrate --noinput
./manage.py collectstatic --noinput --traceback -v 3
./manage.py foo_create_test_data --traceback -v 3
./manage.py runserver 0.0.0.0:8001 --traceback -v 3
