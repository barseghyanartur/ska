import pytest
from pytest_codeblock.constants import CODEBLOCK_MARK


# Modify test item during collection
def pytest_collection_modifyitems(config, items):
    for item in items:
        if item.get_closest_marker(CODEBLOCK_MARK):
            # All `pytest-codeblock` tests are automatically assigned
            # a `codeblock` marker, which can be used for customisation.
            # In the example below we add an additional `documentation`
            # marker to `pytest-codeblock` tests.
            item.add_marker(pytest.mark.documentation)
        if item.get_closest_marker("mock_request"):
            ...


# Setup before test runs
def pytest_runtest_setup(item):
    if item.get_closest_marker("mock_request"):
        ...


# Teardown after the test ends
def pytest_runtest_teardown(item, nextitem):
    if item.get_closest_marker("mock_request"):
        ...
