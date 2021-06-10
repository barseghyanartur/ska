#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.testing")
    sys.path.insert(0, os.path.abspath("src"))
    sys.path.insert(0, "examples/simple")
    from IPython import start_ipython

    start_ipython(argv=[])


if __name__ == "__main__":
    sys.exit(main())
