from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")
F = TypeVar("F")


class CRUDRepository(ABC, Generic[T, F]):
    @abstractmethod
    def create(self, obj: T) -> T:
        pass

    @abstractmethod
    def get_all(self, offset: int = 0, limit: int = 100) -> list[T]:
        pass

    @abstractmethod
    def get_by_id(self, obj_id: int) -> T | None:
        pass

    @abstractmethod
    def delete(self, obj: T):
        pass

    @abstractmethod
    def count(self, filter: F):
        pass

    @abstractmethod
    def get_filtered(self, filter: F, offset: int = 0, limit: int = 100) -> list[T]:
        pass
