from sqlmodel import Session
from app.models.orm.user import User, UserFilter, UserSort
from app.repositories.base_repository import BaseRepository
from app.repositories.strategies.generic_filter_strategy import GenericFilterStrategy
from app.repositories.strategies.generic_sort_strategy import GenericSortStrategy


class UserRepository(BaseRepository[User, UserFilter, UserSort]):
    def __init__(self, session: Session):
        filter_strategy = GenericFilterStrategy(User)
        sort_strategy = GenericSortStrategy(model_class=User, default_sort="name")
        super().__init__(session, User, filter_strategy, sort_strategy)
