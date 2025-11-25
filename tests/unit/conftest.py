import pytest
from unittest.mock import Mock
from app.repositories.hero_repository import HeroRepository
from app.services.hero_service import HeroService


@pytest.fixture
def mock_repository():
    """Mock del repositorio para tests unitarios"""
    return Mock(spec=HeroRepository)


@pytest.fixture
def hero_service(mock_repository):
    """Servicio con repositorio mockeado"""
    return HeroService(repository=mock_repository)
