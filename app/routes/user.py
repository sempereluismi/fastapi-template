from fastapi import APIRouter, Query, Depends, status
from app.models.orm.user import UserFilter, UserSort, UserPut, UserPatch, UserCreate
from app.services.user_service import get_user_service, UserService
from app.utils.response import ResponseBuilder
from uuid import UUID


user_router = APIRouter(tags=["users"])


@user_router.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    result = service.create_user(user)
    return ResponseBuilder.success(data=result, message="User created", status_code=201)


@user_router.get("/users")
def read_useres(
    service: UserService = Depends(get_user_service),
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
    filter_model = UserFilter.from_string(filter)
    sort_model = UserSort.from_string(sort)

    result = service.get_useres_filtered(
        filter=filter_model, offset=offset, limit=limit, sort=sort_model
    )
    total = service.count(filter_model)

    return ResponseBuilder.paginated(
        data=result, page=page, size=size, total=total, message="useres list"
    )


@user_router.get("/users/{user_id}")
def read_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    result = service.get_user_by_id(user_id=user_id)
    return ResponseBuilder.success(data=result, message="user detail")


@user_router.delete("/users/{user_id}")
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_id(user_id=user_id)
    service.delete_user(user=user)
    return ResponseBuilder.success(message="user deleted")


@user_router.put("/users/{user_id}")
def update_user_put(
    user_id: UUID,
    updated_user: UserPut,
    service: UserService = Depends(get_user_service),
):
    result = service.update_user_put(user_id=user_id, updated_user=updated_user)
    return ResponseBuilder.success(data=result, message="user updated (PUT)")


@user_router.patch("/users/{user_id}")
def update_user_patch(
    user_id: UUID,
    partial_update: UserPatch,
    service: UserService = Depends(get_user_service),
):
    update_dict = partial_update.model_dump(exclude_unset=True)
    result = service.update_user_patch(user_id=user_id, partial_update=update_dict)
    return ResponseBuilder.success(data=result, message="user updated (PATCH)")
