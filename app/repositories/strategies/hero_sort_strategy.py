from sqlmodel import select
from app.abstractions.filters.sort_strategy import ISortStrategy
from app.models.orm.hero import Hero, HeroSort
from app.enums.sort import SortDirection


class HeroSortStrategy(ISortStrategy[Hero, HeroSort]):
    """Estrategia de ordenamiento específica para Hero"""

    def apply(self, query: select, sort_model: HeroSort | None = None) -> select:
        if not sort_model or not sort_model.fields:
            return query.order_by(Hero.id)

        field_mapping = Hero.get_field_mapping()

        order_clauses = []
        for field_enum, direction in sort_model.fields:
            field_attr = field_mapping.get(field_enum.value, Hero.id)

            if direction == SortDirection.DESC:
                order_clauses.append(field_attr.desc())
            else:
                order_clauses.append(field_attr.asc())

        return query.order_by(*order_clauses)
