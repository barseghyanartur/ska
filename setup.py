import os
from setuptools import setup, find_packages

try:
  readme = open(os.path.join(os.path.dirname(__file__), 'readme.rst')).read()
except:
  readme = ''

version = '0.1'

setup(
    name = 'ska',
    version = version,
    description = ("Signing requests using symmetric-key algorithm."),
    long_description = readme,
    classifiers = [
        "Programming Language :: Python",
        "Environment :: Web Environment",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
    ],
    keywords = 'signing http requests, symmetric-key algorithm, python',
    author = 'Artur Barseghyan',
    author_email = 'artur.barseghyan@gmail.com',
    package_dir = {'':'src'},
    packages = find_packages(where='./src'),
    install_requires = ['',]
)
