from sqlmodel import Session, select
from app.models.orm.hero import Hero, HeroFilter, HeroSort
from app.repositories.base_repository import BaseRepository
from app.enums.sort import SortDirection


class HeroRepository(BaseRepository[Hero, HeroFilter, HeroSort]):
    def __init__(self, session: Session):
        super().__init__(session, Hero)

    def _apply_filters(
        self, query: select, filter: HeroFilter | None = None
    ) -> select:
        if not filter:
            return query

        if filter.name:
            query = query.where(Hero.name.ilike(f"%{filter.name}%"))
        if filter.age:
            query = query.where(Hero.age == filter.age)

        return query

    def _apply_sorting(self, query: select, sort: HeroSort | None = None) -> select:
        if not sort:
            return query.order_by(Hero.id)

        field_mapping = self.model_class.get_field_mapping()
        field_attr = field_mapping.get(sort.field.value, Hero.id)

        if sort.direction == SortDirection.DESC:
            return query.order_by(field_attr.desc())
        return query.order_by(field_attr.asc())
