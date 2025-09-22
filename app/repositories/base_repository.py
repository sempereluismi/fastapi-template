from abc import ABC, abstractmethod
from sqlmodel import Session, select, func
from typing import TypeVar, Generic, Type

T = TypeVar("T")
FilterType = TypeVar("FilterType")
SortType = TypeVar("SortType")


class BaseRepository(Generic[T, FilterType, SortType], ABC):
    def __init__(self, session: Session, model_class: Type[T]):
        self.session = session
        self.model_class = model_class

    def create(self, entity: T) -> T:
        self.session.add(entity)
        self.session.commit()
        self.session.refresh(entity)
        return entity

    def get_by_id(self, entity_id: int) -> T | None:
        return self.session.get(self.model_class, entity_id)

    def get_all(
        self, offset: int = 0, limit: int = 100, sort: SortType | None = None
    ) -> list[T]:
        query = select(self.model_class)
        query = self._apply_sorting(query, sort)
        return self.session.exec(query.offset(offset).limit(limit)).all()

    def get_filtered(
        self,
        filter: FilterType,
        offset: int = 0,
        limit: int = 100,
        sort: SortType | None = None,
    ) -> list[T]:
        query = select(self.model_class)
        query = self._apply_filters(query, filter)
        query = self._apply_sorting(query, sort)
        return self.session.exec(query.offset(offset).limit(limit)).all()

    def count(self, filter: FilterType | None = None) -> int:
        """Cuenta el total de elementos después del filtrado"""
        query = select(func.count(self.model_class.id))
        if filter:
            query = self._apply_filters(query, filter)
        return self.session.exec(query).one()

    def delete(self, entity: T):
        self.session.delete(entity)
        self.session.commit()

    @abstractmethod
    def _apply_filters(
        self, query: select, filter: FilterType | None = None
    ) -> select:
        pass

    @abstractmethod
    def _apply_sorting(self, query: select, sort: SortType | None = None) -> select:
        pass
