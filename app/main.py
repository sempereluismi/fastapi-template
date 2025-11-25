from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from contextlib import asynccontextmanager
from app.db.database import db
from app.routes.test import test_router
from app.exceptions.base import AppException
from app.utils.response import ResponseBuilder
from app.core.config import config
from loguru import logger
import traceback


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title=config.APP_NAME, debug=config.DEBUG)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")

    logger.warning(f"Validation error on {request.url.path}: {errors}")
    return ResponseBuilder.error(
        errors=errors, message="Validation Error", status_code=422
    )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Maneja excepciones de negocio personalizadas"""
    logger.warning(f"App exception on {request.url.path}: {exc.message}")
    return ResponseBuilder.error(
        errors=[exc.message], message="Error", status_code=exc.status_code
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    """Maneja errores de base de datos"""
    logger.error(f"Database error on {request.url.path}: {str(exc)}")

    if config.DEBUG:
        error_msg = str(exc)
    else:
        error_msg = "A database error occurred"

    return ResponseBuilder.error(
        errors=[error_msg], message="Database Error", status_code=500
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Maneja ValueError (errores de validación de negocio)"""
    logger.warning(f"ValueError on {request.url.path}: {str(exc)}")
    return ResponseBuilder.error(
        errors=[str(exc)], message="Invalid Value", status_code=400
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Captura todas las excepciones no manejadas"""
    logger.error(f"Unhandled exception on {request.url.path}: {str(exc)}")
    logger.error(traceback.format_exc())

    if config.DEBUG:
        error_msg = f"{type(exc).__name__}: {str(exc)}"
        errors = [error_msg, traceback.format_exc()]
    else:
        errors = ["An unexpected error occurred"]

    return ResponseBuilder.error(
        errors=errors, message="Internal Server Error", status_code=500
    )


app.include_router(test_router)


@app.get("/")
async def root():
    return {"app_name": config.APP_NAME, "status": "OK"}


@app.get("/health")
async def health():
    return "OK"
