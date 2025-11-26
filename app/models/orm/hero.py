from sqlmodel import Field
from app.models.orm.base import BaseSQLModel
from app.models.mixins.sortable_mixin import SortableMixin
from app.models.mixins.filterable_mixin import FilterableMixin
from pydantic import BaseModel


class Hero(BaseSQLModel, SortableMixin, FilterableMixin, table=True):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


HeroFilterField, HeroFilter = Hero.create_filter_classes(
    exclude_fields={"created_at", "updated_at"}
)

HeroSortField, HeroSort = Hero.create_sort_classes()


class HeroCreate(BaseModel):
    name: str
    age: int | None = None
    secret_name: str


class HeroPut(BaseModel):
    name: str
    age: int
    secret_name: str


class HeroPatch(BaseModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
