from sqlmodel import Field, SQLModel
from pydantic import BaseModel
from typing import Optional


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str


class HeroFilter(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None

    def to_dict(self) -> dict:
        """Retorna solo los campos con valores no None"""
        return {k: v for k, v in self.model_dump().items() if v is not None}
