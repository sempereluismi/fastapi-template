from abc import ABC
from sqlmodel import Session, select, func
from typing import TypeVar, Generic, Type
from app.abstractions.filters.filter_strategy import IFilterStrategy
from app.abstractions.filters.sort_strategy import ISortStrategy
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

T = TypeVar("T")
FilterType = TypeVar("FilterType")
SortType = TypeVar("SortType")


class BaseRepository(Generic[T, FilterType, SortType], ABC):
    def __init__(
        self,
        session: Session,
        model_class: Type[T],
        filter_strategy: IFilterStrategy[T, FilterType],
        sort_strategy: ISortStrategy[T, SortType],
    ):
        self.session = session
        self.model_class = model_class
        self.filter_strategy = filter_strategy
        self.sort_strategy = sort_strategy

    def create(self, entity: T) -> T:
        try:
            self.session.add(entity)
            self.session.commit()
            self.session.refresh(entity)
            return entity
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error creating {self.model_class.__name__}: {str(e)}")
            raise

    def get_by_id(self, entity_id: int) -> T | None:
        return self.session.get(self.model_class, entity_id)

    def get_all(
        self, offset: int = 0, limit: int = 100, sort: SortType | None = None
    ) -> list[T]:
        query = select(self.model_class)
        query = self.sort_strategy.apply(query, sort)
        return self.session.exec(query.offset(offset).limit(limit)).all()

    def get_filtered(
        self,
        filter: FilterType,
        offset: int = 0,
        limit: int = 100,
        sort: SortType | None = None,
    ) -> list[T]:
        try:
            query = select(self.model_class)
            query = self.filter_strategy.apply(query, filter)
            query = self.sort_strategy.apply(query, sort)
            return self.session.exec(query.offset(offset).limit(limit)).all()
        except SQLAlchemyError as e:
            logger.error(f"Error querying {self.model_class.__name__}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_filtered: {str(e)}")
            raise

    def count(self, filter: FilterType | None = None) -> int:
        """Cuenta el total de elementos después del filtrado"""
        query = select(func.count(self.model_class.id))
        if filter:
            query = self.filter_strategy.apply(query, filter)
        return self.session.exec(query).one()

    def delete(self, entity: T):
        self.session.delete(entity)
        self.session.commit()

    def update_put(self, entity_id: int, updated_entity: T) -> T | None:
        try:
            existing_entity = self.get_by_id(entity_id)
            if not existing_entity:
                return None
            for key, value in updated_entity.dict().items():
                setattr(existing_entity, key, value)
            self.session.add(existing_entity)
            self.session.commit()
            self.session.refresh(existing_entity)
            return existing_entity
        except SQLAlchemyError as e:
            self.session.rollback()
            logger.error(f"Error updating {self.model_class.__name__}: {str(e)}")
            raise

    def update_patch(self, entity_id: int, partial_update: dict) -> T | None:
        """Actualiza parcialmente una entidad existente."""
        existing_entity = self.get_by_id(entity_id)
        if not existing_entity:
            return None
        for key, value in partial_update.items():
            setattr(existing_entity, key, value)
        self.session.add(existing_entity)
        self.session.commit()
        self.session.refresh(existing_entity)
        return existing_entity
