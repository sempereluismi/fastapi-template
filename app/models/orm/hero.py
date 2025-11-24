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
    fields: list[tuple[HeroSortField, SortDirection]] = [
        (HeroSortField.ID, SortDirection.ASC)
    ]

    @classmethod
    def from_string(cls, sort_str: str | None = None):
        """
        Parse una cadena de ordenamiento como 'age:desc,name:asc'
        Si no se proporciona, usa el ordenamiento por defecto
        """
        if not sort_str:
            return cls()

        sort_fields = []
        for part in sort_str.split(","):
            part = part.strip()
            if ":" in part:
                field_str, direction_str = part.split(":", 1)
                try:
                    field = HeroSortField(field_str.strip())
                    direction = SortDirection(direction_str.strip().lower())
                    sort_fields.append((field, direction))
                except ValueError:
                    continue
            else:
                try:
                    field = HeroSortField(part)
                    sort_fields.append((field, SortDirection.ASC))
                except ValueError:
                    continue

        return cls(fields=sort_fields) if sort_fields else cls()


class HeroPut(BaseModel):
    name: str
    age: int
    secret_name: str


class HeroPatch(BaseModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None
