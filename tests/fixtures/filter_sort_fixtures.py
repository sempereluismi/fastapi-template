import pytest
from app.models.orm.hero import HeroFilter, HeroFilterField, HeroSort, HeroSortField
from app.enums.filter import FilterOperator
from app.enums.sort import SortDirection


@pytest.fixture
def hero_filter_name_like():
    """Filtro para buscar héroes por nombre (LIKE)"""
    return HeroFilter(filters=[(HeroFilterField.NAME, FilterOperator.LIKE, "Spider")])


@pytest.fixture
def hero_filter_age_gt():
    """Filtro para buscar héroes mayores de cierta edad"""
    return HeroFilter(filters=[(HeroFilterField.AGE, FilterOperator.GT, 30)])


@pytest.fixture
def hero_filter_multiple():
    """Filtro múltiple para búsquedas complejas"""
    return HeroFilter(
        filters=[
            (HeroFilterField.AGE, FilterOperator.GE, 25),
            (HeroFilterField.NAME, FilterOperator.LIKE, "Man"),
        ]
    )


@pytest.fixture
def hero_sort_name_asc():
    """Ordenamiento por nombre ascendente"""
    return HeroSort(sorts=[(HeroSortField.NAME, SortDirection.ASC)])


@pytest.fixture
def hero_sort_age_desc():
    """Ordenamiento por edad descendente"""
    return HeroSort(sorts=[(HeroSortField.AGE, SortDirection.DESC)])


@pytest.fixture
def hero_sort_multiple():
    """Ordenamiento múltiple"""
    return HeroSort(
        sorts=[
            (HeroSortField.AGE, SortDirection.DESC),
            (HeroSortField.NAME, SortDirection.ASC),
        ]
    )
