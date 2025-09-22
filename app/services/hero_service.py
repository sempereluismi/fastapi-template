from fastapi import Depends
from sqlmodel import Session
from app.repositories.hero_repository import HeroRepository
from app.db.database import db
from app.models.hero import Hero, HeroFilter
from app.interfaces.crud_abstract import CRUDRepository
from app.exceptions.hero import HeroNotFoundException


class HeroService:
    def __init__(self, repository: CRUDRepository[Hero, HeroFilter]):
        self.repository = repository

    def create_hero(self, hero: Hero) -> Hero:
        return self.repository.create(hero)

    def get_heroes(self, offset: int = 0, limit: int = 100) -> list[Hero]:
        return self.repository.get_all(offset, limit)

    def get_hero_by_id(self, hero_id: int) -> Hero:
        hero = self.repository.get_by_id(hero_id)
        if not hero:
            raise HeroNotFoundException(hero_id)
        return hero

    def delete_hero(self, hero: Hero):
        self.repository.delete(hero)

    def get_heroes_filtered(
        self, filter: HeroFilter, offset: int = 0, limit: int = 100
    ) -> list[Hero]:
        return self.repository.get_filtered(filter, offset, limit)

    def count(self, filter: HeroFilter | None = None) -> int:
        return len(self.repository.count(filter=filter))


def get_hero_service(session: Session = Depends(db.get_session)) -> HeroService:
    repo = HeroRepository(session)
    return HeroService(repo)
