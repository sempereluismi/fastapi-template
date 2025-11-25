import pytest
from app.models.orm.hero import Hero, HeroCreate


@pytest.fixture
def hero_data():
    """Datos básicos para crear un héroe"""
    return {"name": "Spider-Man", "age": 25, "secret_name": "Peter Parker"}


@pytest.fixture
def hero_create(hero_data):
    """Modelo HeroCreate para pruebas"""
    return HeroCreate(**hero_data)


@pytest.fixture
def hero_instance(hero_data):
    """Instancia de Hero para pruebas"""
    return Hero(**hero_data)


@pytest.fixture
def hero_in_db(session, hero_instance):
    """Hero guardado en la base de datos"""
    session.add(hero_instance)
    session.commit()
    session.refresh(hero_instance)
    return hero_instance


@pytest.fixture
def multiple_heroes(session):
    """Múltiples héroes en la base de datos"""
    heroes = [
        Hero(name="Spider-Man", age=25, secret_name="Peter Parker"),
        Hero(name="Iron Man", age=45, secret_name="Tony Stark"),
        Hero(name="Captain America", age=100, secret_name="Steve Rogers"),
        Hero(name="Black Widow", age=35, secret_name="Natasha Romanoff"),
    ]
    for hero in heroes:
        session.add(hero)
    session.commit()
    for hero in heroes:
        session.refresh(hero)
    return heroes
