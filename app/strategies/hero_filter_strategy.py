from app.interfaces.filter_strategy import FilterStrategy
from app.models.hero import Hero, HeroFilter
from sqlmodel import select


class HeroFilterStrategy(FilterStrategy[Hero, HeroFilter]):
    def apply_filters(self, query: select, filter: HeroFilter | None = None) -> select:
        if filter:
            if filter.name:
                query = query.where(Hero.name == filter.name)
            if filter.age:
                query = query.where(Hero.age == filter.age)
        return query
