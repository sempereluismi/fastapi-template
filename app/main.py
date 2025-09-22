from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from app.db.database import db
from app.routes.test import test_router
from app.exceptions.base import AppException
from app.utils.response import ResponseBuilder
from app.core.config import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan, title=config.APP_NAME, debug=config.DEBUG)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return ResponseBuilder.error(
        errors=[exc.message], message="Error", status_code=exc.status_code
    )


app.include_router(test_router)


@app.get("/")
async def root():
    return {"app_name": config.APP_NAME, "status": "OK"}
