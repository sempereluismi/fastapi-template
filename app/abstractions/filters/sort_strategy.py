from abc import ABC, abstractmethod
from sqlmodel import select
from typing import TypeVar, Generic

T = TypeVar("T")
SortType = TypeVar("SortType")


class ISortStrategy(ABC, Generic[T, SortType]):
    """Estrategia abstracta para aplicar ordenamiento a una query"""

    @abstractmethod
    def apply(self, query: select, sort_model: SortType | None = None) -> select:
        """Aplica el ordenamiento a la query de SQLModel"""
        pass
