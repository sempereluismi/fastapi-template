from app.exceptions.base import AppException


class PageNotFoundException(AppException):
    def __init__(self, page: int):
        super().__init__(f"Requested page {page} is out of range.", status_code=404)
