from pydantic import BaseModel
from typing import Any, Optional


class Status(BaseModel):
    code: int
    message: Optional[str] = None


class Pagination(BaseModel):
    page: int
    size: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool


class SuccessResponse(BaseModel):
    status: Status
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    status: Status
    errors: list[str]
