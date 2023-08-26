#!/usr/bin/env bash
./scripts/clean_up.sh
sphinx-apidoc src/ska --full -o docs -H 'ska' -A 'Artur Barseghyan <artur.barseghyan@gmail.com>' -f -d 20
cp docs/conf.py.distrib docs/conf.py
cp docs/index.rst.distrib docs/index.rst
