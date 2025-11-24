from fastapi import APIRouter, Query, Depends, status
from app.models.orm.hero import (
    Hero,
    HeroFilter,
    HeroSort,
    HeroSortField,
    HeroPut,
    HeroPatch,
)
from app.enums.sort import SortDirection
from app.services.hero_service import get_hero_service, HeroService
from app.utils.response import ResponseBuilder

test_router = APIRouter(prefix="/test", tags=["test"])


@test_router.post("/heroes", status_code=status.HTTP_201_CREATED)
def create_hero(hero: Hero, service: HeroService = Depends(get_hero_service)):
    result = service.create_hero(hero)
    return ResponseBuilder.success(data=result, message="Hero created", status_code=201)


@test_router.get("/heroes")
def read_heroes(
    service: HeroService = Depends(get_hero_service),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    name: str = Query(""),
    age: int = Query(None),
    sort_field: HeroSortField = Query(
        HeroSortField.ID, description="Campo por el cual ordenar"
    ),
    sort_direction: SortDirection = Query(
        SortDirection.ASC, description="Dirección del ordenamiento"
    ),
):
    offset, limit = ResponseBuilder.get_pagination_params(page, size)
    filter = HeroFilter(name=name, age=age)
    sort = HeroSort(field=sort_field, direction=sort_direction)
    result = service.get_heroes_filtered(
        filter=filter, offset=offset, limit=limit, sort=sort
    )
    total = service.count(filter)
    return ResponseBuilder.paginated(
        data=result, page=page, size=size, total=total, message="Heroes list"
    )


@test_router.get("/heroes/{hero_id}")
def read_hero(hero_id: int, service: HeroService = Depends(get_hero_service)):
    result = service.get_hero_by_id(hero_id=hero_id)
    return ResponseBuilder.success(data=result, message="Hero detail")


@test_router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, service: HeroService = Depends(get_hero_service)):
    hero = service.get_hero_by_id(hero_id=hero_id)
    service.delete_hero(hero=hero)
    return ResponseBuilder.success(message="Hero deleted")


@test_router.put("/heroes/{hero_id}")
def update_hero_put(
    hero_id: int,
    updated_hero: HeroPut,
    service: HeroService = Depends(get_hero_service),
):
    result = service.update_hero_put(hero_id=hero_id, updated_hero=updated_hero)
    return ResponseBuilder.success(data=result, message="Hero updated (PUT)")


@test_router.patch("/heroes/{hero_id}")
def update_hero_patch(
    hero_id: int,
    partial_update: HeroPatch,
    service: HeroService = Depends(get_hero_service),
):
    result = service.update_hero_patch(hero_id=hero_id, partial_update=partial_update)
    return ResponseBuilder.success(data=result, message="Hero updated (PATCH)")
