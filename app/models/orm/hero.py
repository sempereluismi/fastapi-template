from sqlmodel import Field
from app.models.orm.base import BaseSQLModel
from app.models.mixins.sortable_mixin import SortableMixin
from pydantic import BaseModel
from typing import Optional


class Hero(BaseSQLModel, SortableMixin, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


class HeroFilter(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None


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
