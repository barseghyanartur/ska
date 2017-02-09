import os
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
except:
    readme = ''

version = '1.6.7'

exec_dirs = [
    'src/ska/bin/',
]

execs = []
for exec_dir in exec_dirs:
    execs += [os.path.join(exec_dir, f) for f in os.listdir(exec_dir)]

setup(
    name='ska',
    version=version,
    description="Sign- and validate- data (dictionaries, strings) using "
                "symmetric-key algorithm.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Security :: Cryptography",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ],
    keywords='sign data, sign (HTTP) request, symmetric-key algorithm '
             'encryption, sign URL, python, django, password-less login '
             'django, password-less authentication backend django',
    author='Artur Barseghyan',
    author_email='artur.barseghyan@gmail.com',
    url='https://github.com/barseghyanartur/ska',
    package_dir={'': 'src'},
    packages=find_packages(where='./src'),
    include_package_data=True,
    package_data={
        'ska': execs,
    },
    scripts=['src/ska/bin/ska-sign-url'],
    install_requires=[
        'six>=1.9',
        'django-nine>=0.1.10',
    ],
    tests_require=[
        'factory_boy',
        'fake-factory',
        'pytest',
        'pytest-django',
        'radar',
    ]
)
