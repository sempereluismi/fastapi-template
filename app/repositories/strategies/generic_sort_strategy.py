from sqlmodel import select
from app.abstractions.filters.sort_strategy import ISortStrategy
from app.enums.sort import SortDirection
from typing import TypeVar, Callable
from pydantic import BaseModel
from loguru import logger

T = TypeVar("T")
SortType = TypeVar("SortType", bound=BaseModel)


class GenericSortStrategy(ISortStrategy[T, SortType]):
    """Estrategia de ordenamiento genérica que funciona con cualquier modelo"""

    def __init__(self, model_class: type[T], default_sort: str | None = None):
        """
        Inicializa la estrategia de ordenamiento.

        Args:
            model_class: Clase del modelo sobre el que se aplicará el ordenamiento
            default_sort: Campo por defecto para ordenar cuando no se especifica ninguno
        """
        self.model_class = model_class
        self.default_sort = default_sort
        self.direction_map: dict[SortDirection, Callable] = {
            SortDirection.ASC: lambda field: field.asc(),
            SortDirection.DESC: lambda field: field.desc(),
        }

    def apply(self, query: select, sort_model: SortType | None = None) -> select:
        """Aplica ordenamiento al query"""

        if sort_model and hasattr(sort_model, "sorts") and sort_model.sorts:
            return self._apply_sorts(query, sort_model.sorts)

        if self.default_sort and hasattr(self.model_class, self.default_sort):
            default_field = getattr(self.model_class, self.default_sort)
            return query.order_by(default_field.asc())

        return query

    def _apply_sorts(self, query: select, sorts: list[tuple]) -> select:
        """
        Aplica lista de ordenamientos al query.

        Args:
            query: Query SQLModel
            sorts: Lista de tuplas (field_enum, direction_enum)

        Returns:
            Query con ordenamiento aplicado
        """
        for field_enum, direction in sorts:
            field_name = field_enum.value

            if not hasattr(self.model_class, field_name):
                logger.warning(f"Invalid sort field ignored: {field_name}")
                continue

            model_field = getattr(self.model_class, field_name)

            try:
                direction_func = self.direction_map.get(direction)
                if direction_func:
                    query = query.order_by(direction_func(model_field))
                else:
                    logger.warning(f"Unsupported sort direction: {direction.value}")
            except Exception as e:
                logger.warning(
                    f"Error applying sort {field_name} {direction.value}: {str(e)}"
                )
                continue

        return query
