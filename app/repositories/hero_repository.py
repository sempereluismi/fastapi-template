from sqlmodel import Session
from app.models.orm.hero import Hero, HeroFilter, HeroSort
from app.repositories.base_repository import BaseRepository
from app.repositories.strategies.hero_filter_strategy import HeroFilterStrategy
from app.repositories.strategies.hero_sort_strategy import HeroSortStrategy


class HeroRepository(BaseRepository[Hero, HeroFilter, HeroSort]):
    def __init__(self, session: Session):
        filter_strategy = HeroFilterStrategy()
        sort_strategy = HeroSortStrategy()
        super().__init__(session, Hero, filter_strategy, sort_strategy)
