from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.db.database import db
from app.routes.test import test_router
from app.exceptions.base import AppException
from app.utils.response import ResponseBuilder
from app.core.config import get_settings
from loguru import logger
import traceback
import sys

config = get_settings()

logger.remove()
logger.add(
    sys.stderr,
    level=config.log_level.upper(),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug(f"Starting {config.app_name}")
    logger.debug(f"Environment: {config.model_config.get('env_file', 'default')}")
    logger.debug(f"Debug mode: {config.debug}")
    logger.debug(f"Log level: {config.log_level}")
    db.create_db_and_tables()
    yield
    logger.debug("Shutting down application")


app = FastAPI(
    lifespan=lifespan, title=config.app_name, debug=config.debug, version=config.version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.debug(f"CORS enabled for origins: {', '.join(config.cors_origins)}")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Maneja errores de validación de Pydantic"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(x) for x in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")

    return ResponseBuilder.error(
        errors=errors, message="Validation Error", status_code=422
    )


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    """Maneja excepciones de negocio personalizadas"""
    return ResponseBuilder.error(
        errors=[exc.message], message="Error", status_code=exc.status_code
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
    if config.debug:
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
    return {"app_name": config.app_name, "status": "OK"}


@app.get("/health")
async def health():
    return "OK"
