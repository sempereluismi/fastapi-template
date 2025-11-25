import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app
from app.db.database import db
from app.core.config import Settings

pytest_plugins = [
    "tests.fixtures.hero_fixtures",
    "tests.fixtures.utils_fixtures",
    "tests.fixtures.filter_sort_fixtures",
    "tests.fixtures.repository_fixtures",
    "tests.fixtures.response_fixtures",
]


@pytest.fixture(name="test_settings")
def test_settings_fixture():
    """Settings específicas para testing"""
    return Settings(
        app_name="FastAPI Template - Testing",
        debug=True,
        database_url="sqlite:///:memory:",
        log_level="DEBUG",
        cors_origins=["*"],
        version="0.1.0",
    )


@pytest.fixture(name="engine")
def engine_fixture():
    """Motor de base de datos en memoria para tests"""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(engine):
    """Sesión de base de datos para tests"""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Cliente de prueba de FastAPI con base de datos de prueba"""

    def get_test_session():
        yield session

    app.dependency_overrides[db.get_session] = get_test_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def reset_database(session: Session):
    """Limpia la base de datos después de cada test"""
    yield
    session.rollback()
