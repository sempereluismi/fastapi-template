from sqlmodel import Session, select
from app.models.hero import Hero, HeroFilter
from app.interfaces.crud_abstract import CRUDRepository


class HeroRepository(CRUDRepository[Hero, HeroFilter]):
    def __init__(self, session: Session):
        self.session = session

    def create(self, hero: Hero) -> Hero:
        self.session.add(hero)
        self.session.commit()
        self.session.refresh(hero)
        return hero

    def get_all(self, offset: int = 0, limit: int = 100) -> list[Hero]:
        return self.session.exec(select(Hero).offset(offset).limit(limit)).all()

    def get_by_id(self, hero_id: int) -> Hero | None:
        return self.session.get(Hero, hero_id)

    def delete(self, hero: Hero):
        self.session.delete(hero)
        self.session.commit()

    def get_filtered(
        self, filter: HeroFilter, offset: int = 0, limit: int = 100
    ) -> list[Hero]:
        query = select(Hero)
        if filter.name:
            query = query.where(Hero.name == filter.name)
        if filter.age:
            query = query.where(Hero.age == filter.age)
        return self.session.exec(query.offset(offset).limit(limit)).all()

    def count(self, filter: HeroFilter | None) -> int:
        query = select(Hero)
        if filter and filter.name:
            query = query.where(Hero.name == filter.name)
        if filter and filter.age:
            query = query.where(Hero.age == filter.age)
        return self.session.exec(query).all()
