from app.models.response import SuccessResponse, Status, Pagination, ErrorResponse
from fastapi.responses import JSONResponse
from app.exceptions.responses import PageNotFoundException
from datetime import datetime


class ResponseBuilder:
    @staticmethod
    def success(data=None, message="OK", status_code=200):
        status = Status(code=status_code, message=message)

        if hasattr(data, "model_dump"):
            data = data.model_dump(mode="json")

        data = ResponseBuilder._serialize_datetime(data)

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

        data = ResponseBuilder._serialize_datetime(data)

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

    @staticmethod
    def _serialize_datetime(data):
        """Convierte objetos datetime a cadenas en estructuras de datos."""
        if isinstance(data, dict):
            return {
                key: ResponseBuilder._serialize_datetime(value)
                for key, value in data.items()
            }
        elif isinstance(data, list):
            return [ResponseBuilder._serialize_datetime(item) for item in data]
        elif isinstance(data, datetime):
            return data.isoformat()
        elif hasattr(data, "model_dump"):
            return data.model_dump(mode="json")
        return data
