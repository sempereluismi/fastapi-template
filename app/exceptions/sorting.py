from app.exceptions.base import AppException


class SortException(AppException):
    """Base exception for sort-related errors"""

    pass


class InvalidSortFormatException(SortException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class InvalidSortFieldException(SortException):
    def __init__(self, field: str, available_fields: list[str]):
        message = f"Invalid sort field: '{field}'. Available fields: {', '.join(available_fields)}"
        super().__init__(message, status_code=400)


class InvalidSortDirectionException(SortException):
    def __init__(self, direction: str):
        message = f"Invalid sort direction: '{direction}'. Available: asc, desc"
        super().__init__(message, status_code=400)
