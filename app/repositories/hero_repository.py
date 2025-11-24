from sqlmodel import Session
from app.models.orm.hero import Hero, HeroFilter, HeroSort
from app.repositories.base_repository import BaseRepository
from app.repositories.strategies.generic_filter_strategy import GenericFilterStrategy
from app.repositories.strategies.generic_sort_strategy import GenericSortStrategy


class HeroRepository(BaseRepository[Hero, HeroFilter, HeroSort]):
    def __init__(self, session: Session):
        filter_strategy = GenericFilterStrategy(Hero)
        sort_strategy = GenericSortStrategy(model_class=Hero, default_sort="name")
        super().__init__(session, Hero, filter_strategy, sort_strategy)
