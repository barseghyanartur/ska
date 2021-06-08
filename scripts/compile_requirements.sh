#!/usr/bin/env bash
cd examples/requirements/
pip-compile common.in "$@"
pip-compile debug.in "$@"
pip-compile deployment.in "$@"
pip-compile dev.in "$@"
pip-compile django_2_2.in "$@"
pip-compile django_3_0.in "$@"
pip-compile django_3_1.in "$@"
pip-compile django_3_2.in "$@"
pip-compile docs.in "$@"
pip-compile style_checkers.in "$@"
pip-compile test.in "$@"
pip-compile testing.in "$@"
