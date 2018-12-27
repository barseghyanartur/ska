#!/usr/bin/env bash
cd examples/simple/
./manage.py shell --settings=settings.dev "$@"
