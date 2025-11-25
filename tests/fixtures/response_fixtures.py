import pytest
from app.models.response import Status, Pagination, SuccessResponse, ErrorResponse


@pytest.fixture
def status_success():
    """Status de respuesta exitosa"""
    return Status(code=200, message="OK")


@pytest.fixture
def status_error():
    """Status de respuesta con error"""
    return Status(code=400, message="Bad Request")


@pytest.fixture
def pagination_first_page():
    """Paginación primera página"""
    return Pagination(page=1, size=10, total=25, pages=3, has_next=True, has_prev=False)


@pytest.fixture
def pagination_last_page():
    """Paginación última página"""
    return Pagination(page=3, size=10, total=25, pages=3, has_next=False, has_prev=True)


@pytest.fixture
def success_response(status_success):
    """Respuesta exitosa genérica"""
    return SuccessResponse(status=status_success, data={"test": "data"})


@pytest.fixture
def error_response(status_error):
    """Respuesta de error genérica"""
    return ErrorResponse(
        status=status_error, errors=["Error message 1", "Error message 2"]
    )
