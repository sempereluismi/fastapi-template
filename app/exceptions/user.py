from app.exceptions.base import AppException
from uuid import UUID


class UserNotFoundException(AppException):
    def __init__(self, user_id: UUID):
        super().__init__(f"User with id {user_id} not found", status_code=404)
