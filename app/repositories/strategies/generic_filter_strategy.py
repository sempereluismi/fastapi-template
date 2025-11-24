from sqlmodel import select
from app.abstractions.filters.filter_strategy import IFilterStrategy
from typing import TypeVar
from pydantic import BaseModel

T = TypeVar("T")
FilterType = TypeVar("FilterType", bound=BaseModel)


class GenericFilterStrategy(IFilterStrategy[T, FilterType]):
    """Estrategia de filtrado genérica que funciona con cualquier modelo"""

    def __init__(self, model_class: type[T]):
        self.model_class = model_class

    def apply(self, query: select, filter_model: FilterType | None = None) -> select:
        if not filter_model:
            return query

        filter_data = filter_model.model_dump(exclude_none=True)

        for field_name, value in filter_data.items():
            if not hasattr(self.model_class, field_name):
                continue

            model_field = getattr(self.model_class, field_name)

            if isinstance(value, str):
                query = query.where(model_field.ilike(f"%{value}%"))
            elif isinstance(value, (int, float, bool)):
                query = query.where(model_field == value)
            elif isinstance(value, list):
                query = query.where(model_field.in_(value))

        return query
