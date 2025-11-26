from app.models.orm.hero import Hero
from uuid import uuid4


class TestHeroRepositoryCreate:
    """Tests para creación de héroes en el repositorio"""

    def test_create_hero_success(self, hero_repository, hero_instance):
        """Debe crear un héroe correctamente"""
        # Act
        created_hero = hero_repository.create(hero_instance)

        # Assert
        assert created_hero.id is not None
        assert created_hero.name == hero_instance.name
        assert created_hero.age == hero_instance.age
        assert created_hero.secret_name == hero_instance.secret_name

    def test_create_hero_persists_in_database(self, hero_repository, session):
        """Debe persistir el héroe en la base de datos"""
        # Arrange
        hero = Hero(name="Thor", age=1500, secret_name="Thor Odinson")

        # Act
        created_hero = hero_repository.create(hero)

        # Assert
        retrieved = session.get(Hero, created_hero.id)
        assert retrieved is not None
        assert retrieved.name == "Thor"


class TestHeroRepositoryGetById:
    """Tests para obtener héroe por ID"""

    def test_get_by_id_existing_hero(self, hero_repository, hero_in_db):
        """Debe retornar el héroe si existe"""
        # Act
        result = hero_repository.get_by_id(hero_in_db.id)

        # Assert
        assert result is not None
        assert result.id == hero_in_db.id
        assert result.name == hero_in_db.name

    def test_get_by_id_non_existing_hero(self, hero_repository):
        """Debe retornar None si el héroe no existe"""
        # Act
        non_existent_uuid = uuid4()
        result = hero_repository.get_by_id(non_existent_uuid)

        # Assert
        assert result is None


class TestHeroRepositoryGetAll:
    """Tests para obtener todos los héroes"""

    def test_get_all_with_no_heroes(self, hero_repository):
        """Debe retornar lista vacía si no hay héroes"""
        # Act
        result = hero_repository.get_all()

        # Assert
        assert result == []

    def test_get_all_with_multiple_heroes(self, hero_repository, multiple_heroes):
        """Debe retornar todos los héroes"""
        # Act
        result = hero_repository.get_all()

        # Assert
        assert len(result) == 4
        assert all(isinstance(hero, Hero) for hero in result)

    def test_get_all_with_pagination(self, hero_repository, multiple_heroes):
        """Debe paginar correctamente"""
        # Act
        result = hero_repository.get_all(offset=1, limit=2)

        # Assert
        assert len(result) == 2

    def test_get_all_with_sort(
        self, hero_repository, multiple_heroes, hero_sort_age_desc
    ):
        """Debe ordenar correctamente"""
        # Act
        result = hero_repository.get_all(sort=hero_sort_age_desc)

        # Assert
        ages = [hero.age for hero in result]
        assert ages == sorted(ages, reverse=True)


class TestHeroRepositoryGetFiltered:
    """Tests para obtener héroes filtrados"""

    def test_get_filtered_by_name(
        self, hero_repository, multiple_heroes, hero_filter_name_like
    ):
        """Debe filtrar por nombre correctamente"""
        # Act
        result = hero_repository.get_filtered(hero_filter_name_like)

        # Assert
        assert len(result) == 1
        assert result[0].name == "Spider-Man"

    def test_get_filtered_by_age(
        self, hero_repository, multiple_heroes, hero_filter_age_gt
    ):
        """Debe filtrar por edad correctamente"""
        # Act
        result = hero_repository.get_filtered(hero_filter_age_gt)

        # Assert
        assert all(hero.age > 30 for hero in result)

    def test_get_filtered_with_multiple_filters(
        self, hero_repository, multiple_heroes, hero_filter_multiple
    ):
        """Debe aplicar múltiples filtros"""
        # Act
        result = hero_repository.get_filtered(hero_filter_multiple)

        # Assert
        assert all(hero.age >= 25 for hero in result)
        assert all("Man" in hero.name for hero in result)

    def test_get_filtered_with_pagination(
        self, hero_repository, multiple_heroes, hero_filter_age_gt
    ):
        """Debe paginar resultados filtrados"""
        # Act
        result = hero_repository.get_filtered(hero_filter_age_gt, offset=0, limit=1)

        # Assert
        assert len(result) == 1

    def test_get_filtered_with_sort(
        self, hero_repository, multiple_heroes, hero_filter_age_gt, hero_sort_name_asc
    ):
        """Debe ordenar resultados filtrados"""
        # Act
        result = hero_repository.get_filtered(
            hero_filter_age_gt, sort=hero_sort_name_asc
        )

        # Assert
        names = [hero.name for hero in result]
        assert names == sorted(names)


class TestHeroRepositoryCount:
    """Tests para contar héroes"""

    def test_count_without_filter(self, hero_repository, multiple_heroes):
        """Debe contar todos los héroes sin filtro"""
        # Act
        count = hero_repository.count()

        # Assert
        assert count == 4

    def test_count_with_filter(
        self, hero_repository, multiple_heroes, hero_filter_age_gt
    ):
        """Debe contar solo héroes filtrados"""
        # Act
        count = hero_repository.count(hero_filter_age_gt)

        # Assert
        assert count == 3  # Iron Man (45), Captain America (100) y Black Widow (35)

    def test_count_empty_repository(self, hero_repository):
        """Debe retornar 0 si no hay héroes"""
        # Act
        count = hero_repository.count()

        # Assert
        assert count == 0


class TestHeroRepositoryDelete:
    """Tests para eliminar héroes"""

    def test_delete_hero_success(self, hero_repository, hero_in_db, session):
        """Debe eliminar el héroe correctamente"""
        # Arrange
        hero_id = hero_in_db.id

        # Act
        hero_repository.delete(hero_in_db)

        # Assert
        deleted = session.get(Hero, hero_id)
        assert deleted is None

    def test_delete_reduces_count(self, hero_repository, multiple_heroes):
        """Debe reducir el contador al eliminar"""
        # Arrange
        initial_count = hero_repository.count()

        # Act
        hero_repository.delete(multiple_heroes[0])

        # Assert
        assert hero_repository.count() == initial_count - 1


class TestHeroRepositoryUpdatePut:
    """Tests para actualización completa (PUT)"""

    def test_update_put_existing_hero(self, hero_repository, hero_in_db):
        """Debe actualizar completamente un héroe existente"""
        # Arrange
        updated_hero = Hero(name="Updated Name", age=99, secret_name="Updated Secret")

        # Act
        result = hero_repository.update_put(hero_in_db.id, updated_hero)

        # Assert
        assert result is not None
        assert result.name == "Updated Name"
        assert result.age == 99
        assert result.secret_name == "Updated Secret"

    def test_update_put_non_existing_hero(self, hero_repository):
        """Debe retornar None si el héroe no existe"""
        # Arrange
        updated_hero = Hero(name="Test", age=25, secret_name="Test")
        non_existent_uuid = uuid4()

        # Act
        result = hero_repository.update_put(non_existent_uuid, updated_hero)

        # Assert
        assert result is None

    def test_update_put_persists_changes(self, hero_repository, hero_in_db, session):
        """Debe persistir los cambios en la base de datos"""
        # Arrange
        original_name = hero_in_db.name
        updated_hero = Hero(
            name="Permanently Updated", age=50, secret_name="New Secret"
        )

        # Act
        hero_repository.update_put(hero_in_db.id, updated_hero)

        # Assert
        session.expire(hero_in_db)
        session.refresh(hero_in_db)
        assert hero_in_db.name == "Permanently Updated"
        assert hero_in_db.name != original_name


class TestHeroRepositoryUpdatePatch:
    """Tests para actualización parcial (PATCH)"""

    def test_update_patch_single_field(self, hero_repository, hero_in_db):
        """Debe actualizar un solo campo"""
        # Arrange
        original_age = hero_in_db.age
        partial_update = {"name": "Patched Name"}

        # Act
        result = hero_repository.update_patch(hero_in_db.id, partial_update)

        # Assert
        assert result is not None
        assert result.name == "Patched Name"
        assert result.age == original_age  # No debe cambiar

    def test_update_patch_multiple_fields(self, hero_repository, hero_in_db):
        """Debe actualizar múltiples campos"""
        # Arrange
        original_secret = hero_in_db.secret_name
        partial_update = {"name": "New Name", "age": 40}

        # Act
        result = hero_repository.update_patch(hero_in_db.id, partial_update)

        # Assert
        assert result is not None
        assert result.name == "New Name"
        assert result.age == 40
        assert result.secret_name == original_secret  # No debe cambiar

    def test_update_patch_non_existing_hero(self, hero_repository):
        """Debe retornar None si el héroe no existe"""
        # Arrange
        partial_update = {"name": "Test"}
        non_existent_uuid = uuid4()

        # Act
        result = hero_repository.update_patch(non_existent_uuid, partial_update)

        # Assert
        assert result is None

    def test_update_patch_persists_changes(self, hero_repository, hero_in_db, session):
        """Debe persistir los cambios parciales"""
        # Arrange
        partial_update = {"age": 77}

        # Act
        hero_repository.update_patch(hero_in_db.id, partial_update)

        # Assert
        session.expire(hero_in_db)
        session.refresh(hero_in_db)
        assert hero_in_db.age == 77
