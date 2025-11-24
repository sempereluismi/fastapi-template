from enum import Enum
from typing import Type
from app.enums.sort import SortDirection


class SortParser:
    """Responsable SOLO de parsear strings a estructura de ordenamiento"""

    @staticmethod
    def parse(
        sort_str: str | None, field_enum: Type[Enum]
    ) -> list[tuple[Enum, SortDirection]]:
        """
        Convierte un string a lista de ordenamientos.

        Args:
            sort_str: String con formato "campo:direccion,campo2:direccion2"
            field_enum: Enum con los campos permitidos

        Returns:
            Lista de tuplas (field_enum, direction_enum)
        """
        if not sort_str:
            return []

        sorts = []
        for part in sort_str.split(","):
            parsed_sort = SortParser._parse_single_sort(part.strip(), field_enum)
            if parsed_sort:
                sorts.append(parsed_sort)

        return sorts

    @staticmethod
    def _parse_single_sort(
        part: str, field_enum: Type[Enum]
    ) -> tuple[Enum, SortDirection] | None:
        """
        Parsea un solo ordenamiento del formato "campo:direccion"

        Args:
            part: String con un solo ordenamiento
            field_enum: Enum con los campos permitidos

        Returns:
            Tupla (field, direction) o None si es inválido
        """
        if not part:
            return None

        parts = part.split(":", 1)  # Split máximo en 2 partes
        if not parts:
            return None

        field_str = parts[0].strip()
        # Si no se especifica dirección, usar ASC por defecto
        direction_str = parts[1].strip() if len(parts) > 1 else "asc"

        try:
            field = field_enum(field_str)
            direction = SortDirection(direction_str)
            return (field, direction)
        except ValueError:
            # Ignorar ordenamientos inválidos (campo o dirección no existe)
            return None