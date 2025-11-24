from sqlmodel import select
from app.abstractions.filters.sort_strategy import ISortStrategy
from app.enums.sort import SortDirection
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T")
SortType = TypeVar("SortType", bound=BaseModel)


class GenericSortStrategy(ISortStrategy[T, SortType]):
    """Estrategia de ordenamiento genérica"""

    def __init__(self, model_class: type[T], default_sort: str = "id"):
        self.model_class = model_class
        self.default_sort = default_sort

    def apply(self, query: select, sort_model: SortType | None = None) -> select:
        if not sort_model or not hasattr(sort_model, "fields") or not sort_model.fields:

            default_field = getattr(self.model_class, self.default_sort)
            return query.order_by(default_field.asc())

        order_clauses = []
        invalid_fields = []

        for field_enum, direction in sort_model.fields:
            field_name = field_enum.value

            if not hasattr(self.model_class, field_name):
                invalid_fields.append(field_name)
                continue

            field_attr = getattr(self.model_class, field_name)

            if direction == SortDirection.DESC:
                order_clauses.append(field_attr.desc())
            else:
                order_clauses.append(field_attr.asc())

        if invalid_fields:
            from loguru import logger
            logger.warning(f"Invalid sort fields ignored: {', '.join(invalid_fields)}")

        return (
            query.order_by(*order_clauses)
            if order_clauses
            else query.order_by(getattr(self.model_class, self.default_sort).asc())
        )
