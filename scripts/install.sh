#!/usr/bin/env bash
reset
python setup.py develop
mkdir -p examples/logs examples/db examples/static examples/tmp examples/media examples/media/foo-images examples/media/static
