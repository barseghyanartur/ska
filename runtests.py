#!/usr/bin/env python
import os
import sys
import pytest
import coverage


def main():
    coverage.process_startup()
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.testing")
    sys.path.insert(0, os.path.abspath('src'))
    sys.path.insert(0, "examples/simple")
    return pytest.main()


if __name__ == '__main__':
    sys.exit(main())
