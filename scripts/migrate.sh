#!/usr/bin/env bash
cd examples/simple/
./manage.py migrate --settings=settings.dev "$@"
