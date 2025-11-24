from sqlmodel import Field
from app.models.orm.base import BaseSQLModel
from pydantic import BaseModel
from typing import Optional
from enum import Enum
from app.enums.sort import SortDirection


class Hero(BaseSQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

    @classmethod
    def get_field_mapping(cls) -> dict[str, any]:
        """Retorna el mapeo de nombres de campos a atributos del modelo"""
        return {
            "id": cls.id,
            "name": cls.name,
            "age": cls.age,
            "secret_name": cls.secret_name,
        }


class HeroFilter(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None


class HeroSortField(str, Enum):
    ID = "id"
    NAME = "name"
    AGE = "age"
    SECRET_NAME = "secret_name"


class HeroSort(BaseModel):
    field: HeroSortField = HeroSortField.ID
    direction: SortDirection = SortDirection.ASC


class HeroPut(BaseModel):
    name: str
    age: int
    secret_name: str


class HeroPatch(BaseModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
