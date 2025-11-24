from enum import Enum
from app.enums.sort import SortDirection


class SortValidationError(ValueError):
    """Error específico para validación de ordenamiento"""

    pass


class SortValidator:
    """Responsable de validar que los ordenamientos sean correctos"""

    @staticmethod
    def validate_sort_tuple(sort_tuple: tuple) -> None:
        """
        Valida que un ordenamiento tenga el formato correcto.

        Args:
            sort_tuple: Tupla (field, direction)

        Raises:
            SortValidationError: Si el ordenamiento es inválido
        """
        if len(sort_tuple) != 2:
            raise SortValidationError(
                f"Sort must have 2 elements: (field, direction). Got: {sort_tuple}"
            )

        field, direction = sort_tuple

        SortValidator._validate_field(field)
        SortValidator._validate_direction(direction)

    @staticmethod
    def _validate_field(field) -> None:
        """Valida que el campo sea un Enum"""
        if not isinstance(field, Enum):
            raise SortValidationError(
                f"Field must be an Enum. Got: {type(field).__name__}"
            )

    @staticmethod
    def _validate_direction(direction) -> None:
        """Valida que la dirección sea un SortDirection"""
        if not isinstance(direction, SortDirection):
            raise SortValidationError(
                f"Direction must be a SortDirection. Got: {type(direction).__name__}"
            )

    @staticmethod
    def validate_sort_list(sorts: list[tuple]) -> None:
        """
        Valida una lista completa de ordenamientos.

        Args:
            sorts: Lista de tuplas (field, direction)

        Raises:
            SortValidationError: Si algún ordenamiento es inválido
        """
        for sort_item in sorts:
            SortValidator.validate_sort_tuple(sort_item)
