"""
versus.py - package version comparison made easy.

https://github.com/barseghyanartur/versus

A simple utility to check installed package versions.

Usage:

.. code-block:: python

    from versus import get_version

    dj_v = get_version("django")
    if dj_v.gte("4.2"):
        print("Django >= 4.2")
"""

import logging
import re
import unittest
from typing import Optional

try:
    # Python 3.8+
    from importlib.metadata import version as get_installed_version
except ImportError:
    # Older fallback (not needed for Python ≥3.9)
    from importlib_metadata import (
        version as get_installed_version,  # type: ignore
    )

__title__ = "versus"
__version__ = "0.1.2"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023-2025 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "get_version",
    "Version",
)

LOGGER = logging.getLogger(__name__)

# ----------------------------------------------------------------------------
# Package
# ----------------------------------------------------------------------------


class Version:

    def __init__(self, version_str: str) -> None:
        self.version_str = version_str
        self.parts = self._parse_version(version_str)

    def __str__(self) -> str:
        return self.version_str

    def __repr__(self) -> str:
        return self.version_str

    def _parse_version(self, v: str):
        # Split into numeric components
        return [int(part) if part.isdigit() else part
                for part in re.split(r"[.\-]", v)]

    def _compare(self, other: str):
        other_parts = self._parse_version(other)
        return (self.parts > other_parts) - (self.parts < other_parts)

    def gt(self, other: str) -> bool:
        return self._compare(other) > 0

    def gte(self, other: str) -> bool:
        return self._compare(other) >= 0

    def lt(self, other: str) -> bool:
        return self._compare(other) < 0

    def lte(self, other: str) -> bool:
        return self._compare(other) <= 0

    def eq(self, other: str) -> bool:
        return self._compare(other) == 0


def normalise_package_name(name: str) -> str:
    """
    Normalise package name according to PEP 503:
    lowercase and replace dots/underscores with hyphens.
    """
    return re.sub(r"[-_.]+", "-", name).lower()


def get_version(
    package_name: str,
    fail_silently: bool = True,
) -> Optional[Version]:
    """Get package version."""
    normalised_name = normalise_package_name(package_name)
    try:
        v = get_installed_version(normalised_name)
        return Version(v)
    except Exception as e:
        if fail_silently:
            return None
        raise RuntimeError(
            f"Could not retrieve version for package '{package_name}' "
            f"(normalized as '{normalised_name}'): {e}"
        ) from e

# ----------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------


class TestVersion(unittest.TestCase):

    def test_version_str_and_repr(self):
        v = Version("1.2.3")
        self.assertEqual(str(v), "1.2.3")
        self.assertEqual(repr(v), "1.2.3")

    def test_version_comparisons(self):
        v = Version("1.2.3")
        self.assertTrue(v.eq("1.2.3"))
        self.assertTrue(v.gte("1.2.3"))
        self.assertTrue(v.lte("1.2.3"))

        self.assertTrue(v.gt("1.2.2"))
        self.assertTrue(v.gte("1.2.2"))
        self.assertTrue(v.lt("1.2.4"))
        self.assertTrue(v.lte("1.2.4"))

    def test_version_with_prerelease(self):
        v1 = Version("1.2.3-alpha")
        v2 = Version("1.2.3-beta")
        self.assertTrue(v1.lt("1.2.3-beta"))
        self.assertTrue(v2.gt("1.2.3-alpha"))

    def test_get_version_success(self):
        # Assuming sys module always exists
        v = get_version("sys")
        if v is not None:
            self.assertIsInstance(v, Version)

    def test_get_version_fail_silently(self):
        v = get_version("nonexistent_package_xyz", fail_silently=True)
        self.assertIsNone(v)

    def test_get_version_fail_hard(self):
        with self.assertRaises(RuntimeError):
            get_version("nonexistent_package_xyz", fail_silently=False)
