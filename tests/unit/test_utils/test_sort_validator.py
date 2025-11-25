import pytest
from enum import Enum
from app.utils.sorting.sort_validator import SortValidator, SortValidationError
from app.enums.sort import SortDirection


class TestSortValidator:
    """Tests para el validador de ordenamiento"""

    def test_validate_sort_tuple_success(self, mock_sort_field):
        """Debe validar correctamente una tupla de ordenamiento válida"""
        # Arrange
        sort_tuple = (mock_sort_field.NAME, SortDirection.ASC)

        # Act & Assert (no debe lanzar excepción)
        SortValidator.validate_sort_tuple(sort_tuple)

    def test_validate_sort_tuple_invalid_length(self, mock_sort_field):
        """Debe lanzar error si la tupla no tiene 2 elementos"""
        # Arrange
        invalid_tuple = (mock_sort_field.NAME,)  # Solo 1 elemento

        # Act & Assert
        with pytest.raises(SortValidationError, match="Sort must have 2 elements"):
            SortValidator.validate_sort_tuple(invalid_tuple)

    def test_validate_sort_tuple_field_not_enum(self):
        """Debe lanzar error si el campo no es un Enum"""
        # Arrange
        invalid_tuple = ("name", SortDirection.ASC)  # String en lugar de Enum

        # Act & Assert
        with pytest.raises(SortValidationError, match="Field must be an Enum"):
            SortValidator.validate_sort_tuple(invalid_tuple)

    def test_validate_sort_tuple_direction_not_sort_direction(self, mock_sort_field):
        """Debe lanzar error si la dirección no es SortDirection"""
        # Arrange
        invalid_tuple = (
            mock_sort_field.NAME,
            "asc",
        )  # String en lugar de SortDirection

        # Act & Assert
        with pytest.raises(
            SortValidationError, match="Direction must be a SortDirection"
        ):
            SortValidator.validate_sort_tuple(invalid_tuple)

    def test_validate_sort_list_success(self, mock_sort_field):
        """Debe validar correctamente una lista de ordenamientos válidos"""
        # Arrange
        sorts = [
            (mock_sort_field.NAME, SortDirection.ASC),
            (mock_sort_field.AGE, SortDirection.DESC),
        ]

        # Act & Assert (no debe lanzar excepción)
        SortValidator.validate_sort_list(sorts)

    def test_validate_sort_list_empty(self):
        """Debe validar correctamente una lista vacía"""
        # Arrange
        sorts = []

        # Act & Assert (no debe lanzar excepción)
        SortValidator.validate_sort_list(sorts)

    def test_validate_sort_list_with_invalid_item(self, mock_sort_field):
        """Debe lanzar error si algún elemento de la lista es inválido"""
        # Arrange
        sorts = [
            (mock_sort_field.NAME, SortDirection.ASC),
            ("age", SortDirection.DESC),  # Campo inválido
        ]

        # Act & Assert
        with pytest.raises(SortValidationError):
            SortValidator.validate_sort_list(sorts)

    def test_validate_direction_desc(self, mock_sort_field):
        """Debe validar correctamente la dirección DESC"""
        # Arrange
        sort_tuple = (mock_sort_field.AGE, SortDirection.DESC)

        # Act & Assert (no debe lanzar excepción)
        SortValidator.validate_sort_tuple(sort_tuple)

    def test_validate_multiple_fields(self, mock_sort_field):
        """Debe validar correctamente múltiples campos diferentes"""
        # Arrange
        sorts = [
            (mock_sort_field.ID, SortDirection.ASC),
            (mock_sort_field.NAME, SortDirection.DESC),
            (mock_sort_field.AGE, SortDirection.ASC),
        ]

        # Act & Assert (no debe lanzar excepción)
        SortValidator.validate_sort_list(sorts)

    def test_validate_sort_tuple_with_wrong_enum_type(self, mock_sort_field):
        """Debe lanzar error si se usa un Enum pero no del tipo correcto para direction"""

        # Arrange
        class WrongEnum(str, Enum):
            WRONG = "wrong"

        invalid_tuple = (mock_sort_field.NAME, WrongEnum.WRONG)

        # Act & Assert
        with pytest.raises(
            SortValidationError, match="Direction must be a SortDirection"
        ):
            SortValidator.validate_sort_tuple(invalid_tuple)
