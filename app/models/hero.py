from sqlmodel import Field, SQLModel
from typing import Optional


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


class HeroFilter:
    def __init__(self, name: Optional[str] = None, age: Optional[int] = None):
        self.name = name
        self.age = age
