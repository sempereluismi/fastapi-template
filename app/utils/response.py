from app.models.response import SuccessResponse, Status, Pagination, ErrorResponse
from fastapi.responses import JSONResponse
from app.exceptions.responses import PageNotFoundException


class ResponseBuilder:
    @staticmethod
    def success(data=None, message="OK", status_code=200):
        status = Status(code=status_code, message=message)
        envelope = SuccessResponse(status=status, data=data)
        return JSONResponse(status_code=status_code, content=envelope.model_dump())

    @staticmethod
    def error(errors: list[str], message="", status_code=500):
        status = Status(code=status_code, message=message)
        envelope = ErrorResponse(status=status, errors=errors)
        return JSONResponse(status_code=status_code, content=envelope.model_dump())

    @staticmethod
    def paginated(
        data, page: int, size: int, total: int, message="OK", status_code=200
    ):
        pages = (total + size - 1) // size
        if page > pages and total > 0:
            raise PageNotFoundException(page=page)
        pagination = Pagination(
            page=page,
            size=size,
            total=total,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1,
        )
        status = Status(code=status_code, message=message)
        envelope = SuccessResponse(
            status=status, data={"items": data, "pagination": pagination.model_dump()}
        )
        return JSONResponse(status_code=status_code, content=envelope.model_dump())

    @staticmethod
    def get_pagination_params(page: int = 1, page_size: int = 10):
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10
        offset = (page - 1) * page_size
        limit = page_size
        return offset, limit
