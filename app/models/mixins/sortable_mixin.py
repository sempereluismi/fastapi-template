from typing import get_type_hints, Type, Any, cast
from enum import Enum
from pydantic import BaseModel
from app.enums.sort import SortDirection


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
            fields: list[tuple[Any, SortDirection]] = [
                (list(SortFieldEnumType)[0], SortDirection.ASC)
            ]

            @classmethod
            def from_string(cls, sort_str: str | None = None) -> "DynamicSort":
                if not sort_str:
                    return cls()

                sort_fields = []
                for part in sort_str.split(","):
                    part = part.strip()
                    if ":" in part:
                        field_str, direction_str = part.split(":", 1)
                        try:
                            field = SortFieldEnumType(field_str.strip())
                            direction = SortDirection(direction_str.strip().lower())
                            sort_fields.append((field, direction))
                        except ValueError:
                            continue
                    else:
                        try:
                            field = SortFieldEnumType(part)
                            sort_fields.append((field, SortDirection.ASC))
                        except ValueError:
                            continue

                return cls(fields=sort_fields) if sort_fields else cls()

        DynamicSort.__name__ = f"{cls.__name__}Sort"
        DynamicSort.__qualname__ = f"{cls.__name__}Sort"

        return SortFieldEnumType, DynamicSort
