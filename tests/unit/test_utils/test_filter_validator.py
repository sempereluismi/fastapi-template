import pytest
from enum import Enum
from app.utils.filters.filter_validator import FilterValidator, FilterValidationError
from app.enums.filter import FilterOperator


class TestFilterValidator:
    """Tests para el validador de filtros"""

    def test_validate_filter_tuple_success(self, mock_filter_field):
        """Debe validar correctamente una tupla de filtro válida"""
        # Arrange
        filter_tuple = (mock_filter_field.NAME, FilterOperator.EQ, "test")

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_invalid_length(self, mock_filter_field):
        """Debe lanzar error si la tupla no tiene 3 elementos"""
        # Arrange
        invalid_tuple = (mock_filter_field.NAME, FilterOperator.EQ)

        # Act & Assert
        with pytest.raises(FilterValidationError, match="Filter must have 3 elements"):
            FilterValidator.validate_filter_tuple(invalid_tuple)

    def test_validate_filter_tuple_field_not_enum(self):
        """Debe lanzar error si el campo no es un Enum"""
        # Arrange
        invalid_tuple = ("name", FilterOperator.EQ, "test")

        # Act & Assert
        with pytest.raises(FilterValidationError, match="Field must be an Enum"):
            FilterValidator.validate_filter_tuple(invalid_tuple)

    def test_validate_filter_tuple_operator_not_filter_operator(
        self, mock_filter_field
    ):
        """Debe lanzar error si el operador no es FilterOperator"""
        # Arrange
        invalid_tuple = (mock_filter_field.NAME, "eq", "test")

        # Act & Assert
        with pytest.raises(
            FilterValidationError, match="Operator must be a FilterOperator"
        ):
            FilterValidator.validate_filter_tuple(invalid_tuple)

    def test_validate_filter_tuple_is_null_with_value(self, mock_filter_field):
        """Debe lanzar error si IS_NULL tiene un valor"""
        # Arrange
        invalid_tuple = (mock_filter_field.NAME, FilterOperator.IS_NULL, "something")

        # Act & Assert
        with pytest.raises(FilterValidationError, match="should not have a value"):
            FilterValidator.validate_filter_tuple(invalid_tuple)

    def test_validate_filter_tuple_is_null_without_value(self, mock_filter_field):
        """Debe validar correctamente IS_NULL sin valor"""
        # Arrange
        filter_tuple = (mock_filter_field.NAME, FilterOperator.IS_NULL, None)

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_is_not_null_without_value(self, mock_filter_field):
        """Debe validar correctamente IS_NOT_NULL sin valor"""
        # Arrange
        filter_tuple = (mock_filter_field.NAME, FilterOperator.IS_NOT_NULL, None)

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_in_with_list(self, mock_filter_field):
        """Debe validar correctamente IN con una lista"""
        # Arrange
        filter_tuple = (mock_filter_field.NAME, FilterOperator.IN, ["value1", "value2"])

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_in_with_tuple(self, mock_filter_field):
        """Debe validar correctamente IN con una tupla"""
        # Arrange
        filter_tuple = (mock_filter_field.NAME, FilterOperator.IN, ("value1", "value2"))

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_in_without_list(self, mock_filter_field):
        """Debe lanzar error si IN no tiene una lista o tupla"""
        # Arrange
        invalid_tuple = (mock_filter_field.NAME, FilterOperator.IN, "single_value")

        # Act & Assert
        with pytest.raises(
            FilterValidationError, match="requires a list or tuple value"
        ):
            FilterValidator.validate_filter_tuple(invalid_tuple)

    def test_validate_filter_tuple_not_in_with_list(self, mock_filter_field):
        """Debe validar correctamente NOT_IN con una lista"""
        # Arrange
        filter_tuple = (
            mock_filter_field.NAME,
            FilterOperator.NOT_IN,
            ["value1", "value2"],
        )

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_gt_with_int(self, mock_filter_field):
        """Debe validar correctamente GT con un entero"""
        # Arrange
        filter_tuple = (mock_filter_field.AGE, FilterOperator.GT, 18)

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_gt_with_float(self, mock_filter_field):
        """Debe validar correctamente GT con un float"""
        # Arrange
        filter_tuple = (mock_filter_field.AGE, FilterOperator.GT, 18.5)

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_gt_with_string(self, mock_filter_field):
        """Debe lanzar error si GT tiene un string"""
        # Arrange
        invalid_tuple = (mock_filter_field.AGE, FilterOperator.GT, "18")

        # Act & Assert
        with pytest.raises(FilterValidationError, match="requires numeric value"):
            FilterValidator.validate_filter_tuple(invalid_tuple)

    def test_validate_filter_tuple_gte_with_numeric(self, mock_filter_field):
        """Debe validar correctamente GE con valor numérico"""
        # Arrange
        filter_tuple = (mock_filter_field.AGE, FilterOperator.GE, 18)

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_lt_with_numeric(self, mock_filter_field):
        """Debe validar correctamente LT con valor numérico"""
        # Arrange
        filter_tuple = (mock_filter_field.AGE, FilterOperator.LT, 65)

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_lte_with_numeric(self, mock_filter_field):
        """Debe validar correctamente LE con valor numérico"""
        # Arrange
        filter_tuple = (mock_filter_field.AGE, FilterOperator.LE, 65)

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_eq_with_string(self, mock_filter_field):
        """Debe validar correctamente EQ con cualquier tipo de valor"""
        # Arrange
        filter_tuple = (mock_filter_field.NAME, FilterOperator.EQ, "John")

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_ne_with_value(self, mock_filter_field):
        """Debe validar correctamente NE con cualquier tipo de valor"""
        # Arrange
        filter_tuple = (mock_filter_field.NAME, FilterOperator.NE, "Jane")

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_like_with_string(self, mock_filter_field):
        """Debe validar correctamente LIKE con un string"""
        # Arrange
        filter_tuple = (mock_filter_field.NAME, FilterOperator.LIKE, "john")

        # Act & Assert (no debe lanzar excepción)
        FilterValidator.validate_filter_tuple(filter_tuple)

    def test_validate_filter_tuple_with_wrong_enum_type(self, mock_filter_field):
        """Debe lanzar error si se usa un Enum pero no del tipo correcto para operator"""

        # Arrange
        class WrongEnum(str, Enum):
            WRONG = "wrong"

        invalid_tuple = (mock_filter_field.NAME, WrongEnum.WRONG, "value")

        # Act & Assert
        with pytest.raises(
            FilterValidationError, match="Operator must be a FilterOperator"
        ):
            FilterValidator.validate_filter_tuple(invalid_tuple)
