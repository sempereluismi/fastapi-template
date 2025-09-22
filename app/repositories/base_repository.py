from sqlmodel import Session, select, func
from app.interfaces.crud_abstract import CRUDRepository
from app.interfaces.filter_strategy import FilterStrategy
from typing import TypeVar, Generic, Type

T = TypeVar("T")
F = TypeVar("F")


class BaseRepository(CRUDRepository[T, F], Generic[T, F]):
    def __init__(
        self,
        session: Session,
        model_class: Type[T],
        filter_strategy: FilterStrategy[T, F],
    ):
        self.session = session
        self.model_class = model_class
        self.filter_strategy = filter_strategy

    def _build_filtered_query(self, filter: F | None = None):
        """Método genérico que funciona para cualquier modelo"""
        query = select(self.model_class)
        return self.filter_strategy.apply_filters(query, filter)

    def create(self, obj: T) -> T:
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def get_all(self, offset: int = 0, limit: int = 100) -> list[T]:
        return self.session.exec(
            select(self.model_class).offset(offset).limit(limit)
        ).all()

    def get_by_id(self, obj_id: int) -> T | None:
        return self.session.get(self.model_class, obj_id)

    def delete(self, obj: T):
        self.session.delete(obj)
        self.session.commit()

    def get_filtered(self, filter: F, offset: int = 0, limit: int = 100) -> list[T]:
        query = self._build_filtered_query(filter)
        return self.session.exec(query.offset(offset).limit(limit)).all()

    def count(self, filter: F | None = None) -> int:
        query = select(func.count(self.model_class.id))
        query = self.filter_strategy.apply_filters(query, filter)
        return self.session.exec(query).one()
