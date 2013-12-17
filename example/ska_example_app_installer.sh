wget -O ska_example_app_installer.tar.gz https://github.com/barseghyanartur/ska/archive/stable.tar.gz
virtualenv ska
source ska/bin/activate
mkdir ska_example_app_installer/
tar -xvf ska_example_app_installer.tar.gz -C ska_example_app_installer
cd ska_example_app_installer/ska-stable/example/example/
pip install Django
pip install -r ../requirements.txt
pip install -e git+https://github.com/barseghyanartur/ska@stable#egg=ska
mkdir ../media/
mkdir ../media/static/
mkdir ../static/
mkdir ../db/
mkdir ../logs/
mkdir ../tmp/
cp local_settings.example local_settings.py
./manage.py syncdb --noinput --traceback -v 3
./manage.py migrate --noinput
./manage.py collectstatic --noinput --traceback -v 3
./manage.py foo_create_test_data --traceback -v 3
./manage.py runserver 0.0.0.0:8001 --traceback -v 3