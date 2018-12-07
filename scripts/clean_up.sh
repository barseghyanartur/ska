#!/usr/bin/env bash
find . -name "*.pyc" -exec rm -rf {} \;
find . -name "__pycache__" -exec rm -rf {} \;
find . -name "*.orig" -exec rm -rf {} \;
find . -name "*.py,cover" -exec rm -rf {} \;
find . -name "*.log" -exec rm -rf {} \;
find . -name "*.log.*" -exec rm -rf {} \;
rm -rf build/
rm -rf dist/
rm -rf src/ska.egg-info/
rm -rf .cache/
rm -rf htmlcov/