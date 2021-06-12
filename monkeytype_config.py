import os
from contextlib import contextmanager
import sys
from typing import Iterator

from monkeytype.config import DefaultConfig


class MonkeyConfig(DefaultConfig):
    @contextmanager
    def cli_context(self, command: str) -> Iterator[None]:
        sys.path.insert(0, os.path.abspath("src"))
        sys.path.insert(0, os.path.abspath("examples"))
        sys.path.insert(0, os.path.abspath(os.path.join("examples", "simple")))
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.testing")
        import django

        django.setup()
        yield


CONFIG = MonkeyConfig()
