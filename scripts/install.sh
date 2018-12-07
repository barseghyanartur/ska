#!/usr/bin/env bash
reset
python setup.py develop
mkdir -p example/logs example/db example/static example/tmp example/media example/media/foo-images example/media/static
