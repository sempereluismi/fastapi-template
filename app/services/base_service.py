from typing import Generic, TypeVar, Type
from uuid import UUID
from loguru import logger

ModelType = TypeVar("ModelType")
FilterType = TypeVar("FilterType")
SortType = TypeVar("SortType")
CreateSchemaType = TypeVar("CreateSchemaType")
PutSchemaType = TypeVar("PutSchemaType")
PatchSchemaType = TypeVar("PatchSchemaType")
ExceptionType = TypeVar("ExceptionType", bound=Exception)


class BaseService(
    Generic[
        ModelType,
        FilterType,
        SortType,
        CreateSchemaType,
        PutSchemaType,
        PatchSchemaType,
        ExceptionType,
    ]
):
    def __init__(
        self,
        repository,
        not_found_exception: Type[ExceptionType],
        model_class: Type[ModelType],
    ):
        self.repository = repository
        self.not_found_exception = not_found_exception
        self.model_class = model_class

    def create(self, data: CreateSchemaType) -> ModelType:
        logger.info(f"Creating new {self.model_class.__name__}: {data}")
        entity = self.model_class(**data.model_dump())
        created = self.repository.create(entity)
        logger.info(f"{self.model_class.__name__} created: {created.id}")
        return created

    def get_by_id(self, entity_id: UUID) -> ModelType:
        entity = self.repository.get_by_id(entity_id)
        if not entity:
            raise self.not_found_exception(entity_id)
        return entity

    def get_filtered(
        self,
        filter: FilterType,
        offset: int = 0,
        limit: int = 100,
        sort: SortType | None = None,
    ) -> list[ModelType]:
        return self.repository.get_filtered(filter, offset, limit, sort)

    def count(self, filter: FilterType | None = None) -> int:
        return self.repository.count(filter=filter)

    def update_put(self, entity_id: UUID, data: PutSchemaType) -> ModelType:
        logger.info(f"Updating {self.model_class.__name__} {entity_id} (PUT)")
        updated = self.repository.update_put(entity_id, data)
        if not updated:
            raise self.not_found_exception(entity_id)
        return updated

    def update_patch(self, entity_id: UUID, data: dict) -> ModelType:
        logger.info(f"Updating {self.model_class.__name__} {entity_id} (PATCH)")
        updated = self.repository.update_patch(entity_id, data)
        if not updated:
            raise self.not_found_exception(entity_id)
        return updated

    def delete(self, entity: ModelType):
        self.repository.delete(entity)
