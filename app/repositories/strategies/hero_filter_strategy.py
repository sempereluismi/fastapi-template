from sqlmodel import select
from app.abstractions.filters.filter_strategy import IFilterStrategy
from app.models.orm.hero import Hero, HeroFilter


class HeroFilterStrategy(IFilterStrategy[Hero, HeroFilter]):
    """Estrategia de filtrado específica para Hero"""

    def apply(self, query: select, filter_model: HeroFilter | None = None) -> select:
        if not filter_model:
            return query

        if filter_model.name:
            query = query.where(Hero.name.ilike(f"%{filter_model.name}%"))

        if filter_model.age:
            query = query.where(Hero.age == filter_model.age)

        return query
