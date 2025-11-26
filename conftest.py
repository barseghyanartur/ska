from types import SimpleNamespace

import pytest
from django.http import Http404 as DjangoHttp404
from pytest_codeblock.constants import CODEBLOCK_MARK


@pytest.fixture
def http_request_factory():
    """
    Returns a function that creates a simple namespace object
    with a 'GET' attribute set to the provided dictionary.
    """
    def _factory(get_data: dict):
        # Creates an object like: object(GET={'key': 'value'})
        return SimpleNamespace(GET=get_data)
    return _factory


@pytest.fixture
def http_request(http_request_factory):
    test_data = {"param1": "value1", "signature": "mock-sig"}
    return http_request_factory(test_data)


@pytest.fixture
def Http404():  # noqa
    return DjangoHttp404


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
