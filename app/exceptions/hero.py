from app.exceptions.base import AppException


class HeroNotFoundException(AppException):
    def __init__(self, hero_id: int):
        super().__init__(f"Hero with id {hero_id} not found", status_code=404)
