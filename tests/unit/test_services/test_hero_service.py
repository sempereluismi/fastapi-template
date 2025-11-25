import pytest
from app.models.orm.hero import Hero, HeroCreate
from app.exceptions.hero import HeroNotFoundException


class TestHeroServiceCreate:
    """Tests para la creación de héroes"""

    def test_create_hero_with_negative_age_raises_error(
        self, hero_service, mock_repository
    ):
        """Debe lanzar error si la edad es negativa"""
        # Arrange
        invalid_hero = HeroCreate(name="Test", age=-5, secret_name="Test")

        # Act & Assert
        with pytest.raises(ValueError, match="age cannot be negative"):
            hero_service.create_hero(invalid_hero)


class TestHeroServiceActivate:
    """Tests para activación de héroes"""

    def test_activate_hero_success(self, hero_service, mock_repository):
        """Debe activar un héroe adulto correctamente"""
        # Arrange
        hero = Hero(id=1, name="Test", age=25, secret_name="Test")
        mock_repository.get_by_id.return_value = hero

        # Act
        result = hero_service.activate_hero(1)

        # Assert
        assert result.id == 1
        mock_repository.get_by_id.assert_called_once_with(1)

    def test_activate_hero_underage_raises_error(self, hero_service, mock_repository):
        """Debe lanzar error si el héroe es menor de edad"""
        # Arrange
        underage_hero = Hero(id=1, name="Test", age=15, secret_name="Test")
        mock_repository.get_by_id.return_value = underage_hero

        # Act & Assert
        with pytest.raises(ValueError, match="must be 18 or older"):
            hero_service.activate_hero(1)


class TestHeroServiceGetById:
    """Tests para obtener héroe por ID"""

    def test_get_hero_by_id_success(self, hero_service, mock_repository):
        """Debe retornar un héroe existente"""
        # Arrange
        hero = Hero(id=1, name="Test", age=25, secret_name="Test")
        mock_repository.get_by_id.return_value = hero

        # Act
        result = hero_service.get_hero_by_id(1)

        # Assert
        assert result.id == 1
        assert result.name == "Test"

    def test_get_hero_by_id_not_found(self, hero_service, mock_repository):
        """Debe lanzar excepción si el héroe no existe"""
        # Arrange
        mock_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HeroNotFoundException):
            hero_service.get_hero_by_id(999)


class TestHeroServiceRetire:
    """Tests para retirar héroes"""

    def test_retire_hero_success(self, hero_service, mock_repository):
        """Debe retirar un héroe mayor de 65 años"""
        # Arrange
        hero = Hero(id=1, name="Old Hero", age=70, secret_name="Test")
        mock_repository.get_by_id.return_value = hero

        # Act
        hero_service.retire_hero(1)

        # Assert
        mock_repository.delete.assert_called_once_with(hero)

    def test_retire_hero_early_retirement(self, hero_service, mock_repository):
        """Debe permitir retirar héroe menor de 65 (con advertencia)"""
        # Arrange
        hero = Hero(id=1, name="Young Hero", age=40, secret_name="Test")
        mock_repository.get_by_id.return_value = hero

        # Act
        hero_service.retire_hero(1)

        # Assert
        mock_repository.delete.assert_called_once_with(hero)

    def test_retire_hero_not_found(self, hero_service, mock_repository):
        """Debe lanzar excepción si el héroe no existe"""
        # Arrange
        mock_repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(HeroNotFoundException):
            hero_service.retire_hero(999)


class TestHeroServiceGetHeroes:
    """Tests para obtener lista de héroes"""

    def test_get_heroes_success(self, hero_service, mock_repository):
        """Debe retornar lista de héroes"""
        # Arrange
        heroes = [
            Hero(id=1, name="Hero1", age=25, secret_name="Secret1"),
            Hero(id=2, name="Hero2", age=30, secret_name="Secret2"),
        ]
        mock_repository.get_all.return_value = heroes

        # Act
        result = hero_service.get_heroes()

        # Assert
        assert len(result) == 2
        assert result == heroes

    def test_get_heroes_with_pagination(self, hero_service, mock_repository):
        """Debe pasar parámetros de paginación al repositorio"""
        # Arrange
        mock_repository.get_all.return_value = []

        # Act
        hero_service.get_heroes(offset=10, limit=5)

        # Assert
        mock_repository.get_all.assert_called_once_with(10, 5, None)


class TestHeroServiceGetHeroesFiltered:
    """Tests para obtener héroes filtrados"""

    def test_get_heroes_filtered_success(
        self, hero_service, mock_repository, hero_filter_name_like
    ):
        """Debe retornar héroes filtrados"""
        # Arrange
        heroes = [Hero(id=1, name="Spider-Man", age=25, secret_name="Peter Parker")]
        mock_repository.get_filtered.return_value = heroes

        # Act
        result = hero_service.get_heroes_filtered(hero_filter_name_like)

        # Assert
        assert len(result) == 1
        assert result[0].name == "Spider-Man"

    def test_get_heroes_filtered_with_pagination_and_sort(
        self, hero_service, mock_repository, hero_filter_age_gt, hero_sort_name_asc
    ):
        """Debe pasar todos los parámetros al repositorio"""
        # Arrange
        mock_repository.get_filtered.return_value = []

        # Act
        hero_service.get_heroes_filtered(
            hero_filter_age_gt, offset=5, limit=10, sort=hero_sort_name_asc
        )

        # Assert
        mock_repository.get_filtered.assert_called_once_with(
            hero_filter_age_gt, 5, 10, hero_sort_name_asc
        )


class TestHeroServiceCount:
    """Tests para contar héroes"""

    def test_count_without_filter(self, hero_service, mock_repository):
        """Debe contar todos los héroes"""
        # Arrange
        mock_repository.count.return_value = 10

        # Act
        result = hero_service.count()

        # Assert
        assert result == 10

    def test_count_with_filter(self, hero_service, mock_repository, hero_filter_age_gt):
        """Debe contar héroes filtrados"""
        # Arrange
        mock_repository.count.return_value = 5

        # Act
        result = hero_service.count(hero_filter_age_gt)

        # Assert
        assert result == 5
        mock_repository.count.assert_called_once_with(filter=hero_filter_age_gt)


class TestHeroServiceUpdatePut:
    """Tests para actualización completa (PUT)"""

    def test_update_hero_put_success(self, hero_service, mock_repository):
        """Debe actualizar un héroe existente con PUT"""
        # Arrange
        updated_hero = Hero(id=1, name="Updated", age=30, secret_name="Updated Secret")
        mock_repository.update_put.return_value = updated_hero

        # Act
        result = hero_service.update_hero_put(1, updated_hero)

        # Assert
        assert result.name == "Updated"
        assert result.age == 30
        mock_repository.update_put.assert_called_once_with(1, updated_hero)

    def test_update_hero_put_not_found(self, hero_service, mock_repository):
        """Debe lanzar excepción si el héroe no existe"""
        # Arrange
        updated_hero = Hero(id=999, name="Test", age=25, secret_name="Test")
        mock_repository.update_put.return_value = None

        # Act & Assert
        with pytest.raises(HeroNotFoundException):
            hero_service.update_hero_put(999, updated_hero)


class TestHeroServiceUpdatePatch:
    """Tests para actualización parcial (PATCH)"""

    def test_update_hero_patch_success(self, hero_service, mock_repository):
        """Debe actualizar parcialmente un héroe existente"""
        # Arrange
        partial_update = {"name": "Patched Name"}
        updated_hero = Hero(id=1, name="Patched Name", age=25, secret_name="Secret")
        mock_repository.update_patch.return_value = updated_hero

        # Act
        result = hero_service.update_hero_patch(1, partial_update)

        # Assert
        assert result.name == "Patched Name"
        mock_repository.update_patch.assert_called_once_with(1, partial_update)

    def test_update_hero_patch_multiple_fields(self, hero_service, mock_repository):
        """Debe actualizar múltiples campos parcialmente"""
        # Arrange
        partial_update = {"name": "New Name", "age": 40}
        updated_hero = Hero(id=1, name="New Name", age=40, secret_name="Secret")
        mock_repository.update_patch.return_value = updated_hero

        # Act
        result = hero_service.update_hero_patch(1, partial_update)

        # Assert
        assert result.name == "New Name"
        assert result.age == 40

    def test_update_hero_patch_not_found(self, hero_service, mock_repository):
        """Debe lanzar excepción si el héroe no existe"""
        # Arrange
        partial_update = {"name": "Test"}
        mock_repository.update_patch.return_value = None

        # Act & Assert
        with pytest.raises(HeroNotFoundException):
            hero_service.update_hero_patch(999, partial_update)


class TestHeroServiceDeleteHero:
    """Tests para eliminar héroe"""

    def test_delete_hero_success(self, hero_service, mock_repository, hero_instance):
        """Debe eliminar un héroe correctamente"""
        # Act
        hero_service.delete_hero(hero_instance)

        # Assert
        mock_repository.delete.assert_called_once_with(hero_instance)
