import pytest
from unittest.mock import Mock
from app.repositories.hero_repository import HeroRepository


@pytest.fixture
def mock_session():
    """Mock de sesión de base de datos"""
    return Mock()


@pytest.fixture
def mock_filter_strategy():
    """Mock de estrategia de filtrado"""
    strategy = Mock()
    strategy.apply.side_effect = lambda query, _: query
    return strategy


@pytest.fixture
def mock_sort_strategy():
    """Mock de estrategia de ordenamiento"""
    strategy = Mock()
    strategy.apply.side_effect = lambda query, _: query
    return strategy


@pytest.fixture
def hero_repository(session):
    """Repositorio de héroes con base de datos real para tests"""
    return HeroRepository(session)
