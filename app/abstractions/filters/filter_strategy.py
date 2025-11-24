from abc import ABC, abstractmethod
from sqlmodel import select
from typing import TypeVar, Generic

T = TypeVar("T")
FilterType = TypeVar("FilterType")


class IFilterStrategy(ABC, Generic[T, FilterType]):
    """Estrategia abstracta para aplicar filtros a una query"""

    @abstractmethod
    def apply(self, query: select, filter_model: FilterType) -> select:
        """Aplica los filtros a la query de SQLModel"""
        pass
