#!/usr/bin/env bash
reset
pycodestyle src/ska/ --exclude src/ska/contrib/django/ska/migrations/,src/ska/contrib/django/ska/south_migrations/
