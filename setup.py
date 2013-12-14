import os
from setuptools import setup, find_packages

try:
  readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
  readme = ''

version = '1.1'

setup(
    name = 'ska',
    version = version,
    description = ("Signing (HTTP) requests using symmetric-key algorithm."),
    long_description = readme,
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Topic :: Security :: Cryptography",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    keywords = 'signing (HTTP) requests, symmetric-key algorithm, signing URLs, python',
    author = 'Artur Barseghyan',
    author_email = 'artur.barseghyan@gmail.com',
    url = 'https://github.com/barseghyanartur/ska',
    package_dir = {'':'src'},
    packages = find_packages(where='./src'),
    include_package_data = True,
    install_requires = [
        #'six==1.4.1',
        'six>=1.1.0',
        #'six>=1.4.0'
    ]
)
