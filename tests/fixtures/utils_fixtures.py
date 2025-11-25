import pytest
from enum import Enum


class MockSortField(str, Enum):
    """Enum de prueba para tests de ordenamiento"""

    NAME = "name"
    AGE = "age"
    ID = "id"


class MockFilterField(str, Enum):
    """Enum de prueba para tests de filtros"""

    NAME = "name"
    AGE = "age"
    ID = "id"


@pytest.fixture
def mock_sort_field():
    """Fixture que provee el Enum de campos para ordenamiento"""
    return MockSortField


@pytest.fixture
def mock_filter_field():
    """Fixture que provee el Enum de campos para filtrado"""
    return MockFilterField
