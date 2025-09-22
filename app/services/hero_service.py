from fastapi import Depends
from sqlmodel import Session
from app.repositories.hero_repository import HeroRepository
from app.db.database import db
from app.models.hero import Hero, HeroFilter, HeroSort
from app.abstractions.repositories.crud_abstract import CRUDRepository
from app.exceptions.hero import HeroNotFoundException
from loguru import logger


class HeroService:
    def __init__(self, repository: CRUDRepository[Hero, HeroFilter]):
        self.repository = repository

    def create_hero(self, hero: Hero) -> Hero:
        if hero.age and hero.age < 0:
            raise ValueError("Hero age cannot be negative")

        logger.info(f"Creating new hero: {hero.name}")

        created_hero = self.repository.create(hero)

        logger.info(f"Hero created successfully with ID: {created_hero.id}")

        return created_hero

    def activate_hero(self, hero_id: int) -> Hero:
        """Ejemplo de lógica de negocio real"""
        hero = self.get_hero_by_id(hero_id)

        if hero.age and hero.age < 18:
            raise ValueError("Heroes must be 18 or older to be activated")

        logger.info(f"Hero {hero.name} has been activated")

        return hero

    def get_hero_by_id(self, hero_id: int) -> Hero:
        hero = self.repository.get_by_id(hero_id)
        if not hero:
            raise HeroNotFoundException(hero_id)
        return hero

    def retire_hero(self, hero_id: int) -> None:
        """Ejemplo de proceso de negocio complejo"""
        hero = self.get_hero_by_id(hero_id)

        if hero.age and hero.age < 65:
            logger.warning(f"Early retirement for hero {hero.name}")

        self.repository.delete(hero)
        logger.info(f"Hero {hero.name} has been retired")

    def get_heroes(
        self, offset: int = 0, limit: int = 100, sort: HeroSort | None = None
    ) -> list[Hero]:
        return self.repository.get_all(offset, limit, sort)

    def delete_hero(self, hero: Hero):
        self.repository.delete(hero)

    def get_heroes_filtered(
        self,
        filter: HeroFilter,
        offset: int = 0,
        limit: int = 100,
        sort: HeroSort | None = None,
    ) -> list[Hero]:
        return self.repository.get_filtered(filter, offset, limit, sort)

    def count(self, filter: HeroFilter | None = None) -> int:
        return self.repository.count(filter=filter)


def get_hero_service(session: Session = Depends(db.get_session)) -> HeroService:
    repo = HeroRepository(session)
    return HeroService(repo)
