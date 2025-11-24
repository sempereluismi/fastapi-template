from typing import get_type_hints, Type, Any, cast
from enum import Enum
from pydantic import BaseModel, field_validator
from app.enums.filter import FilterOperator
from app.utils.filters.filter_parser import FilterParser
from app.utils.filters.filter_validator import FilterValidator


class FilterableMixin:
    """Mixin que genera automáticamente clases de filtrado para cualquier modelo"""

    @classmethod
    def create_filter_classes(
        cls, exclude_fields: set[str] | None = None
    ) -> tuple[Type[Enum], Type[BaseModel]]:
        """
        Genera automáticamente FilterField (Enum) y Filter (BaseModel) para el modelo.

        Args:
            exclude_fields: Campos a excluir del filtrado (ej: {'created_at', 'updated_at'})

        Returns:
            tuple[Type[Enum], Type[BaseModel]]: (FilterFieldEnum, FilterModel)
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
        FilterFieldEnum = Enum(f"{cls.__name__}FilterField", enum_fields, type=str)

        FilterFieldEnumType = cast(Type[Enum], FilterFieldEnum)

        class DynamicFilter(BaseModel):
            """
            Sistema de filtros dinámico.

            Formato de filters: lista de tuplas (campo, operador, valor)
            Ejemplo: [(FilterField.NAME, FilterOperator.LIKE, "Spider"),
                      (FilterField.AGE, FilterOperator.GT, 18)]
            """

            filters: list[tuple[Any, FilterOperator, Any]] = []

            @field_validator("filters")
            @classmethod
            def validate_filters(cls, v):
                """Valida que los filtros tengan el formato correcto"""
                for filter_item in v:
                    FilterValidator.validate_filter_tuple(filter_item)
                return v

            @classmethod
            def from_string(cls, filter_str: str | None = None) -> "DynamicFilter":
                """
                Convierte un string a un objeto Filter.

                Formato: "campo:operador:valor,campo2:operador2:valor2"

                Ejemplos:
                - "name:like:Spider" -> name LIKE '%Spider%'
                - "age:gt:18" -> age > 18
                - "age:ge:18,age:le:65" -> age >= 18 AND age <= 65
                - "name:in:Spider,Iron,Thor" -> name IN ('Spider', 'Iron', 'Thor')
                - "age:is_null:" -> age IS NULL

                Operadores disponibles:
                - eq: igual (=)
                - ne: diferente (!=)
                - gt: mayor que (>)
                - ge: mayor o igual (>=)
                - lt: menor que (<)
                - le: menor o igual (<=)
                - like: contiene (LIKE '%valor%')
                - in: en lista (IN)
                - not_in: no en lista (NOT IN)
                - is_null: es nulo (IS NULL)
                - is_not_null: no es nulo (IS NOT NULL)
                """
                filters = FilterParser.parse(filter_str, FilterFieldEnumType)
                return cls(filters=filters)

        DynamicFilter.__name__ = f"{cls.__name__}Filter"
        DynamicFilter.__qualname__ = f"{cls.__name__}Filter"

        return FilterFieldEnumType, DynamicFilter
