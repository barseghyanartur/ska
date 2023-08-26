import os

from setuptools import find_packages, setup

try:
    readme = open(os.path.join(os.path.dirname(__file__), "README.rst")).read()
except:
    readme = ""

version = "1.10"

setup(
    name="ska",
    version=version,
    description="Sign- and validate- data (dictionaries, strings) using "
    "symmetric-key algorithm.",
    long_description=readme,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
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
    project_urls={
        "Bug Tracker": "https://github.com/barseghyanartur/ska/issues",
        "Documentation": "https://ska.readthedocs.io/",
        "Source Code": "https://github.com/barseghyanartur/ska",
        "Changelog": "https://ska.readthedocs.io/en/latest/changelog.html",
    },
    license="GPL-2.0-only OR LGPL-2.1-or-later",
    entry_points={
        "console_scripts": ["ska-sign-url = ska.generate_signed_url:main"]
    },
    install_requires=[],
    extras_require={
        "django": ["django-nine>=0.2.4"],
        "django-constance": ["django-constance", "django-nine>=0.2.4"],
        "djangorestframework": ["djangorestframework", "django-nine>=0.2.4"],
        "drf-jwt": ["drf-jwt", "django-nine>=0.2.4"],
    },
    tests_require=[
        "factory_boy",
        "faker",
        "pytest",
        "pytest-django",
        "mock",
        "beautifulsoup4",
        "soupsieve",
        "coverage",
    ],
)
