from typing import get_type_hints, Type, Any, cast
from enum import Enum
from pydantic import BaseModel, field_validator
from app.enums.sort import SortDirection
from app.utils.sorting.sort_parser import SortParser
from app.utils.sorting.sort_validator import SortValidator


class SortableMixin:
    """Mixin que genera automáticamente clases de ordenamiento para cualquier modelo"""

    @classmethod
    def create_sort_classes(
        cls, exclude_fields: set[str] | None = None
    ) -> tuple[Type[Enum], Type[BaseModel]]:
        """
        Genera automáticamente SortField (Enum) y Sort (BaseModel) para el modelo.

        Args:
            exclude_fields: Campos a excluir del ordenamiento (ej: {'created_at', 'updated_at'})

        Returns:
            tuple[Type[Enum], Type[BaseModel]]: (SortFieldEnum, SortModel)
        """
        if exclude_fields is None:
            exclude_fields = set()

        if hasattr(cls, "model_fields"):
            field_names = [
                name for name in cls.model_fields.keys() if name not in exclude_fields
            ]
        else:
            field_names = [
                name
                for name in get_type_hints(cls).keys()
                if name not in exclude_fields and not name.startswith("_")
            ]

        enum_fields = {name.upper(): name for name in field_names}
        SortFieldEnum = Enum(f"{cls.__name__}SortField", enum_fields, type=str)

        SortFieldEnumType = cast(Type[Enum], SortFieldEnum)

        class DynamicSort(BaseModel):
            """
            Sistema de ordenamiento dinámico.

            Formato de sorts: lista de tuplas (campo, dirección)
            Ejemplo: [(SortField.NAME, SortDirection.ASC),
                      (SortField.AGE, SortDirection.DESC)]
            """

            sorts: list[tuple[Any, SortDirection]] = []

            @field_validator("sorts")
            @classmethod
            def validate_sorts(cls, v):
                """Valida que los ordenamientos tengan el formato correcto"""
                SortValidator.validate_sort_list(v)
                return v

            @classmethod
            def from_string(cls, sort_str: str | None = None) -> "DynamicSort":
                """
                Convierte un string a un objeto Sort.

                Formato: "campo:direccion,campo2:direccion2"

                Ejemplos:
                - "name:asc" -> ORDER BY name ASC
                - "age:desc" -> ORDER BY age DESC
                - "name:asc,age:desc" -> ORDER BY name ASC, age DESC
                - "name" -> ORDER BY name ASC (dirección por defecto)

                Direcciones disponibles:
                - asc: ascendente (A->Z, 0->9)
                - desc: descendente (Z->A, 9->0)
                """
                sorts = SortParser.parse(sort_str, SortFieldEnumType)
                return cls(sorts=sorts)

        DynamicSort.__name__ = f"{cls.__name__}Sort"
        DynamicSort.__qualname__ = f"{cls.__name__}Sort"

        return SortFieldEnumType, DynamicSort
