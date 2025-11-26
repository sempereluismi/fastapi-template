from fastapi import APIRouter, Query, Depends, status
from app.models.orm.hero import HeroFilter, HeroSort, HeroPut, HeroPatch, HeroCreate
from app.services.hero_service import get_hero_service, HeroService
from app.utils.response import ResponseBuilder
from uuid import UUID

test_router = APIRouter(prefix="/test", tags=["test"])


@test_router.post("/heroes", status_code=status.HTTP_201_CREATED)
def create_hero(hero: HeroCreate, service: HeroService = Depends(get_hero_service)):
    result = service.create_hero(hero)
    return ResponseBuilder.success(data=result, message="Hero created", status_code=201)


@test_router.get("/heroes")
def read_heroes(
    service: HeroService = Depends(get_hero_service),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    filter: str = Query(
        None,
        description="Filtros: 'campo:operador:valor,campo2:operador:valor'. Ej: 'name:like:Spider,age:gt:18'",
    ),
    sort: str = Query(
        None,
        description="Ordenamiento: 'campo:direccion,campo2:direccion'. Ej: 'age:desc,name:asc'",
    ),
):
    offset, limit = ResponseBuilder.get_pagination_params(page, size)
    filter_model = HeroFilter.from_string(filter)
    sort_model = HeroSort.from_string(sort)

    result = service.get_heroes_filtered(
        filter=filter_model, offset=offset, limit=limit, sort=sort_model
    )
    total = service.count(filter_model)

    return ResponseBuilder.paginated(
        data=result, page=page, size=size, total=total, message="Heroes list"
    )


@test_router.get("/heroes/{hero_id}")
def read_hero(hero_id: UUID, service: HeroService = Depends(get_hero_service)):
    result = service.get_hero_by_id(hero_id=hero_id)
    return ResponseBuilder.success(data=result, message="Hero detail")


@test_router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: UUID, service: HeroService = Depends(get_hero_service)):
    hero = service.get_hero_by_id(hero_id=hero_id)
    service.delete_hero(hero=hero)
    return ResponseBuilder.success(message="Hero deleted")


@test_router.put("/heroes/{hero_id}")
def update_hero_put(
    hero_id: UUID,
    updated_hero: HeroPut,
    service: HeroService = Depends(get_hero_service),
):
    result = service.update_hero_put(hero_id=hero_id, updated_hero=updated_hero)
    return ResponseBuilder.success(data=result, message="Hero updated (PUT)")


@test_router.patch("/heroes/{hero_id}")
def update_hero_patch(
    hero_id: UUID,
    partial_update: HeroPatch,
    service: HeroService = Depends(get_hero_service),
):
    update_dict = partial_update.model_dump(exclude_unset=True)
    result = service.update_hero_patch(hero_id=hero_id, partial_update=update_dict)
    return ResponseBuilder.success(data=result, message="Hero updated (PATCH)")
