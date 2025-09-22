from abc import ABC, abstractmethod
from sqlmodel import select
from typing import TypeVar, Generic

T = TypeVar("T")
F = TypeVar("F")


class FilterStrategy(ABC, Generic[T, F]):
    @abstractmethod
    def apply_filters(self, query: select, filter: F | None = None) -> select:
        pass
