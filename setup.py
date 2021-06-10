import os
from setuptools import setup, find_packages

try:
    readme = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()
except:
    readme = ""

version = "1.8.1"

exec_dirs = [
    "src/ska/bin/",
]

execs = []
for exec_dir in exec_dirs:
    execs += [os.path.join(exec_dir, f) for f in os.listdir(exec_dir)]

setup(
    name="ska",
    version=version,
    description="Sign- and validate- data (dictionaries, strings) using "
    "symmetric-key algorithm.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Security :: Cryptography",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or "
        "later (LGPLv2+)",
    ],
    keywords="sign data, sign (HTTP) request, symmetric-key algorithm "
    "encryption, sign URL, python, django, password-less login "
    "django, password-less authentication backend django",
    author="Artur Barseghyan",
    author_email="artur.barseghyan@gmail.com",
    url="https://github.com/barseghyanartur/ska",
    package_dir={"": "src"},
    packages=find_packages(where="./src"),
    include_package_data=True,
    package_data={
        "ska": execs,
    },
    project_urls={
        "Bug Tracker": "https://github.com/barseghyanartur/ska/issues",
        "Documentation": "https://ska.readthedocs.io/",
        "Source Code": "https://github.com/barseghyanartur/ska",
        "Changelog": "https://ska.readthedocs.io/" "en/latest/changelog.html",
    },
    license="GPL-2.0-only OR LGPL-2.1-or-later",
    scripts=["src/ska/bin/ska-sign-url"],
    install_requires=[
        "django-nine>=0.2.4",
    ],
    extras_require={
        "django-constance": ["django-constance"],
        "djangorestframework": ["djangorestframework"],
        "drf-jwt": ["drf-jwt"],
    },
    tests_require=[
        "factory_boy",
        "faker",
        "pytest",
        "pytest-django",
        "radar",
        "mock",
        "beautifulsoup4",
        "soupsieve",
        "coverage",
    ],
)
