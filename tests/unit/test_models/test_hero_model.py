import pytest
from app.models.orm.hero import Hero, HeroCreate, HeroPut, HeroPatch
from uuid import uuid4


class TestHeroModel:
    """Tests para el modelo Hero"""

    def test_hero_creation_with_all_fields(self):
        """Debe crear un héroe con todos los campos"""
        # Arrange & Act
        test_uuid = uuid4()
        hero = Hero(id=test_uuid, name="Spider-Man", age=25, secret_name="Peter Parker")

        # Assert
        assert hero.id == test_uuid
        assert hero.name == "Spider-Man"
        assert hero.age == 25
        assert hero.secret_name == "Peter Parker"

    def test_hero_creation_without_optional_fields(self):
        """Debe crear un héroe sin campos opcionales"""
        # Arrange & Act
        hero = Hero(name="Batman", secret_name="Bruce Wayne")

        # Assert
        assert hero.name == "Batman"
        assert hero.secret_name == "Bruce Wayne"
        assert hero.age is None
        assert hero.id is not None  # UUID se genera automáticamente

    def test_hero_has_timestamps(self):
        """Debe tener timestamps automáticos"""
        # Arrange & Act
        hero = Hero(name="Superman", secret_name="Clark Kent")

        # Assert
        assert hasattr(hero, "created_at")
        assert hasattr(hero, "updated_at")

    def test_hero_model_dump(self):
        """Debe serializar correctamente a dict"""
        # Arrange
        test_uuid = uuid4()
        hero = Hero(id=test_uuid, name="Iron Man", age=45, secret_name="Tony Stark")

        # Act
        data = hero.model_dump()

        # Assert
        assert data["name"] == "Iron Man"
        assert data["age"] == 45
        assert data["secret_name"] == "Tony Stark"
        assert "created_at" in data
        assert "updated_at" in data


class TestHeroCreateModel:
    """Tests para el modelo HeroCreate"""

    def test_hero_create_with_all_fields(self):
        """Debe crear modelo de creación con todos los campos"""
        # Arrange & Act
        hero_data = HeroCreate(name="Hulk", age=35, secret_name="Bruce Banner")

        # Assert
        assert hero_data.name == "Hulk"
        assert hero_data.age == 35
        assert hero_data.secret_name == "Bruce Banner"

    def test_hero_create_without_age(self):
        """Debe permitir crear sin edad"""
        # Arrange & Act
        hero_data = HeroCreate(name="Thor", secret_name="Thor Odinson")

        # Assert
        assert hero_data.name == "Thor"
        assert hero_data.secret_name == "Thor Odinson"
        assert hero_data.age is None

    def test_hero_create_validates_required_fields(self):
        """Debe validar campos requeridos"""
        # Act & Assert
        with pytest.raises(ValueError):
            HeroCreate(name="Test")  # Falta secret_name


class TestHeroPutModel:
    """Tests para el modelo HeroPut"""

    def test_hero_put_with_all_fields(self):
        """Debe crear modelo PUT con todos los campos requeridos"""
        # Arrange & Act
        hero_data = HeroPut(name="Black Widow", age=35, secret_name="Natasha Romanoff")

        # Assert
        assert hero_data.name == "Black Widow"
        assert hero_data.age == 35
        assert hero_data.secret_name == "Natasha Romanoff"

    def test_hero_put_requires_all_fields(self):
        """Debe requerir todos los campos en PUT"""
        # Act & Assert
        with pytest.raises(ValueError):
            HeroPut(name="Test", secret_name="Test")  # Falta age


class TestHeroPatchModel:
    """Tests para el modelo HeroPatch"""

    def test_hero_patch_with_single_field(self):
        """Debe permitir actualización parcial con un solo campo"""
        # Arrange & Act
        hero_data = HeroPatch(name="Captain America")

        # Assert
        assert hero_data.name == "Captain America"
        assert hero_data.age is None
        assert hero_data.secret_name is None

    def test_hero_patch_with_multiple_fields(self):
        """Debe permitir actualización parcial con múltiples campos"""
        # Arrange & Act
        hero_data = HeroPatch(name="Hawkeye", age=40)

        # Assert
        assert hero_data.name == "Hawkeye"
        assert hero_data.age == 40
        assert hero_data.secret_name is None

    def test_hero_patch_all_fields_optional(self):
        """Debe permitir crear HeroPatch sin ningún campo"""
        # Arrange & Act
        hero_data = HeroPatch()

        # Assert
        assert hero_data.name is None
        assert hero_data.age is None
        assert hero_data.secret_name is None
