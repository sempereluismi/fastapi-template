from app.abstractions.repositories.crud_abstract import CRUDRepository
from app.models.orm.user import User, UserCreate, UserSort, UserFilter
from app.repositories.user_repository import UserRepository
from app.exceptions.user import UserNotFoundException
from app.db.database import db
from app.utils.hash import PasswordHasher

from uuid import UUID
from fastapi import Depends
from sqlmodel import Session


class UserService:
    def __init__(self, repository: CRUDRepository):
        self.repository = repository

    def create_user(self, user: UserCreate) -> User:
        user_dict = user.model_dump()
        user_dict["password"] = PasswordHasher.hash_password(user_dict["password"])
        user_entity = User(**user_dict)
        created_user = self.repository.create(user_entity)

        return created_user

    def get_user_by_id(self, user_id: UUID):
        user = self.repository.get_by_id(user_id)

        if not user:
            raise UserNotFoundException(user_id)

        return user

    def get_heroes(
        self,
        offset: int = 0,
        limit: int = 100,
        sort: UserSort | None = None,
    ) -> list[User]:
        return self.repository.get_all(offset, limit, sort)

    def delete_user(self, user: User):
        self.repository.delete(user)

    def get_heroes_filtered(
        self,
        filter: UserFilter,
        offset: int = 0,
        limit: int = 100,
        sort: UserSort | None = None,
    ) -> list[User]:
        return self.repository.get_filtered(filter, offset, limit, sort)

    def count(self, filter: UserFilter | None = None) -> int:
        return self.repository.count(filter=filter)

    def update_hero_put(self, user_id: UUID, updated_user: User) -> User:
        updated_entity = self.repository.update_put(user_id, updated_user)
        if not updated_entity:
            raise UserNotFoundException(user_id)
        return updated_entity

    def update_hero_patch(self, user_id: UUID, partial_update: dict) -> User:
        updated_entity = self.repository.update_patch(user_id, partial_update)
        if not updated_entity:
            raise UserNotFoundException(user_id)
        return updated_entity


def get_user_service(session: Session = Depends(db.get_session)) -> UserService:
    repo = UserRepository(session)
    return UserService(repo)
