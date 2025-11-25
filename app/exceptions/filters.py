from app.exceptions.base import AppException
from app.enums.filter import FilterOperator


class FilterException(AppException):
    """Base exception for filter-related errors"""

    pass


class InvalidFilterFormatException(FilterException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class InvalidFilterFieldException(FilterException):
    def __init__(self, field: str, available_fields: list[str]):
        message = f"Invalid filter field: '{field}'. Available fields: {', '.join(available_fields)}"
        super().__init__(message, status_code=400)


class InvalidFilterOperatorException(FilterException):
    def __init__(self, operator: str):
        operators = [e.value for e in FilterOperator]
        operators_str = ", ".join(operators)
        message = (
            f"Invalid filter operator: '{operator}'. "
            f"Available operators: {operators_str}"
        )
        super().__init__(message, status_code=400)
