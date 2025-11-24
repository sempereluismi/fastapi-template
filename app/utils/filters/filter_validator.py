from enum import Enum
from app.enums.filter import FilterOperator


class FilterValidationError(ValueError):
    """Error específico para validación de filtros"""

    pass


class FilterValidator:
    """Responsable de validar que los filtros sean correctos"""

    @staticmethod
    def validate_filter_tuple(filter_tuple: tuple) -> None:
        """
        Valida que un filtro tenga el formato correcto.

        Args:
            filter_tuple: Tupla (field, operator, value)

        Raises:
            FilterValidationError: Si el filtro es inválido
        """
        if len(filter_tuple) != 3:
            raise FilterValidationError(
                f"Filter must have 3 elements: (field, operator, value). Got: {filter_tuple}"
            )

        field, operator, value = filter_tuple

        FilterValidator._validate_field(field)
        FilterValidator._validate_operator(operator)
        FilterValidator._validate_value(operator, value)

    @staticmethod
    def _validate_field(field) -> None:
        """Valida que el campo sea un Enum"""
        if not isinstance(field, Enum):
            raise FilterValidationError(
                f"Field must be an Enum. Got: {type(field).__name__}"
            )

    @staticmethod
    def _validate_operator(operator) -> None:
        """Valida que el operador sea un FilterOperator"""
        if not isinstance(operator, FilterOperator):
            raise FilterValidationError(
                f"Operator must be a FilterOperator. Got: {type(operator).__name__}"
            )

    @staticmethod
    def _validate_value(operator: FilterOperator, value: any) -> None:
        """Valida que el valor sea apropiado para el operador"""

        if operator in [FilterOperator.IS_NULL, FilterOperator.IS_NOT_NULL]:
            if value is not None:
                raise FilterValidationError(
                    f"Operator {operator.value} should not have a value. Got: {value}"
                )

        elif operator in [FilterOperator.IN, FilterOperator.NOT_IN]:
            if not isinstance(value, (list, tuple)):
                raise FilterValidationError(
                    f"Operator {operator.value} requires a list or tuple value. Got: {type(value).__name__}"
                )

        elif operator in [
            FilterOperator.GT,
            FilterOperator.GE,
            FilterOperator.LT,
            FilterOperator.LE,
        ]:
            if value is not None and not isinstance(value, (int, float)):
                raise FilterValidationError(
                    f"Operator {operator.value} requires numeric value. Got: {type(value).__name__}"
                )
