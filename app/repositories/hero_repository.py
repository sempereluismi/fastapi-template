from sqlmodel import Session
from app.models.hero import Hero, HeroFilter
from app.repositories.base_repository import BaseRepository
from app.strategies.hero_filter_strategy import HeroFilterStrategy


class HeroRepository(BaseRepository[Hero, HeroFilter]):
    def __init__(self, session: Session):
        super().__init__(session, Hero, HeroFilterStrategy())
