#!/usr/bin/env bash
cd examples/requirements/

echo "pip-compile common.in"
uv pip compile ../../pyproject.toml common.in --all-extras -o common.txt "$@"

echo "pip-compile debug.in"
uv pip compile ../../pyproject.toml debug.in --all-extras -o debug.txt "$@"

echo "pip-compile deployment.in"
uv pip compile ../../pyproject.toml deployment.in --all-extras -o deployment.txt "$@"

echo "pip-compile dev.in"
uv pip compile ../../pyproject.toml dev.in --all-extras -o dev.txt "$@"

echo "pip-compile django_4_2.in"
uv pip compile ../../pyproject.toml django_4_2.in --all-extras -o django_4_2.txt "$@"

echo "pip-compile django_5_1.in"
uv pip compile ../../pyproject.toml django_5_1.in --all-extras -o django_5_1.txt "$@"

echo "pip-compile django_5_2.in"
uv pip compile ../../pyproject.toml django_5_2.in --all-extras -o django_5_2.txt "$@"

echo "pip-compile docs.in"
uv pip compile ../../pyproject.toml docs.in --all-extras -o docs.txt "$@"

echo "pip-compile documentation.in"
uv pip compile ../../pyproject.toml documentation.in --all-extras -o documentation.txt "$@"

echo "pip-compile style_checkers.in"
uv pip compile ../../pyproject.toml style_checkers.in --all-extras -o style_checkers.txt "$@"

echo "pip-compile test.in"
uv pip compile ../../pyproject.toml test.in --all-extras -o test.txt "$@"

echo "pip-compile testing.in"
uv pip compile ../../pyproject.toml testing.in --all-extras -o testing.txt "$@"
