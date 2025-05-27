#!/usr/bin/env bash
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "__pycache__" -exec rm -rf {} \;
find . -name "*.orig" -exec rm -rf {} \;
find . -name "*.py,cover" -exec rm -rf {} \;
find . -name "*.log" -exec rm -rf {} \;
find . -name "*.coverage" -exec rm -rf {} \;
find . -name "builddocs.zip" -exec rm -rf {} \;
find . -name "*.log.*" -exec rm -rf {} \;
rm -rf build/
rm -rf builddocs/
rm -rf dist/
rm -rf src/ska.egg-info/
rm -rf .cache/
rm -rf htmlcov/
rm -rf .pytest_cache/
rm -rf examples/logs/
