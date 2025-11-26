from app.exceptions.base import AppException
from uuid import UUID


class HeroNotFoundException(AppException):
    def __init__(self, hero_id: UUID):
        super().__init__(f"Hero with id {hero_id} not found", status_code=404)
