from enum import Enum
from typing import Type
from app.enums.filter import FilterOperator
from app.utils.filters.filter_value_converter import FilterValueConverter
from loguru import logger
from app.exceptions.filters import InvalidFilterFormatException


class FilterParser:
    """Responsable SOLO de parsear strings a estructura de filtros"""

    @staticmethod
    def parse(
        filter_str: str | None, field_enum: Type[Enum]
    ) -> list[tuple[Enum, FilterOperator, any]]:
        """
        Convierte un string a lista de filtros.

        Args:
            filter_str: String con formato "campo:operador:valor,campo2:operador2:valor2"
            field_enum: Enum con los campos permitidos

        Returns:
            Lista de tuplas (field_enum, operator_enum, value)
        """
        if not filter_str:
            return []

        filters = []
        for part in filter_str.split(","):
            parsed_filter = FilterParser._parse_single_filter(part.strip(), field_enum)
            if parsed_filter:
                filters.append(parsed_filter)

        return filters

    @staticmethod
    def _parse_single_filter(
        part: str, field_enum: Type[Enum]
    ) -> tuple[Enum, FilterOperator, any] | None:
        """
        Parsea un solo filtro del formato "campo:operador:valor"

        Args:
            part: String con un solo filtro
            field_enum: Enum con los campos permitidos

        Returns:
            Tupla (field, operator, value) o None si es inválido
        """
        if not part:
            return None

        parts = part.split(":", 2)
        if len(parts) < 2:
            logger.warning(f"Invalid filter format: {part}")
            raise InvalidFilterFormatException(
                f"Filter must have format 'field:operator:value'. Got: {part}"
            )

        field_str = parts[0].strip()
        operator_str = parts[1].strip()
        value_str = parts[2].strip() if len(parts) > 2 else None

        try:
            field = field_enum(field_str)
        except ValueError:
            logger.warning(f"Invalid filter field: {field_str}")
            raise InvalidFilterFormatException(
                f"Invalid field '{field_str}'. Available fields: {[e.value for e in field_enum]}"
            )

        try:
            operator = FilterOperator(operator_str)
        except ValueError:
            logger.warning(f"Invalid operator: {operator_str}")
            raise InvalidFilterFormatException(
                f"Invalid operator '{operator_str}'. Available operators: {[e.value for e in FilterOperator]}"
            )

        value = FilterValueConverter.convert(value_str, operator)
        return (field, operator, value)
