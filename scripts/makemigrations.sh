#!/usr/bin/env bash
cd examples/simple/
./manage.py makemigrations --settings=settings.dev "$@"
