from sqlmodel import select
from app.abstractions.filters.filter_strategy import IFilterStrategy
from app.enums.filter import FilterOperator
from typing import TypeVar, Callable
from pydantic import BaseModel
from loguru import logger


T = TypeVar("T")
FilterType = TypeVar("FilterType", bound=BaseModel)


class GenericFilterStrategy(IFilterStrategy[T, FilterType]):
    """Estrategia de filtrado genérica que funciona con cualquier modelo"""

    def __init__(self, model_class: type[T]):
        self.model_class = model_class
        self.operator_map: dict[FilterOperator, Callable] = {
            FilterOperator.EQ: lambda field, value: field == value,
            FilterOperator.NE: lambda field, value: field != value,
            FilterOperator.GT: lambda field, value: field > value,
            FilterOperator.GE: lambda field, value: field >= value,
            FilterOperator.LT: lambda field, value: field < value,
            FilterOperator.LE: lambda field, value: field <= value,
            FilterOperator.LIKE: lambda field, value: field.ilike(f"%{value}%"),
            FilterOperator.IN: lambda field, value: field.in_(value),
            FilterOperator.NOT_IN: lambda field, value: ~field.in_(value),
            FilterOperator.IS_NULL: lambda field, value: field.is_(None),
            FilterOperator.IS_NOT_NULL: lambda field, value: field.isnot(None),
        }

    def apply(self, query: select, filter_model: FilterType | None = None) -> select:
        if not filter_model and not (
            hasattr(filter_model, "filters") and filter_model.filters
        ):
            return query

        return self._apply_advanced_filters(query, filter_model.filters)

    def _apply_advanced_filters(self, query: select, filters: list) -> select:
        """Aplica filtros usando el nuevo sistema con operadores"""

        for field_enum, operator, value in filters:
            field_name = field_enum.value

            if not hasattr(self.model_class, field_name):
                logger.warning(f"Invalid filter field ignored: {field_name}")
                continue

            if operator == FilterOperator.LIKE and isinstance(value, str):
                value = value.replace("%", "\\%").replace("_", "\\_")

            model_field = getattr(self.model_class, field_name)

            try:
                filter_func = self.operator_map.get(operator)
                if filter_func:
                    query = query.where(filter_func(model_field, value))
                else:
                    logger.warning(f"Unsupported operator: {operator.value}")
            except Exception as e:
                logger.warning(
                    f"Error applying filter {field_name} {operator.value} {value}: {str(e)}"
                )
                continue

        return query
