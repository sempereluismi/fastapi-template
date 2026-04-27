from sqlmodel import Field
from app.models.orm.base import BaseSQLModel
from app.models.mixins.sortable_mixin import SortableMixin
from app.models.mixins.filterable_mixin import FilterableMixin
from pydantic import BaseModel


class User(BaseSQLModel, SortableMixin, FilterableMixin, table=True):
    name: str = Field(index=True)
    password: str = Field(nullable=False)


UserFilterField, UserFilter = User.create_filter_classes(
    exclude_fields={"created_at", "updated_at"}
)

UserSortField, UserSort = User.create_sort_classes()


class UserCreate(BaseModel):
    name: str
    password: str


class UserPut(BaseModel):
    name: str
    password: str


class UserPatch(BaseModel):
    name: str | None = None
    password: str | None = None
