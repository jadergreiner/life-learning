"""Aplicação ASGI da API do LAB01."""

import logging
import os
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.api.routes import router
from src.database.connection import dispose_database, get_engine
from src.database.errors import DatabaseConnectionError, QueryExecutionError
from src.domain.events import EventConflictError, EventValidationError
from src.repositories.accounts import AccountNotFoundError

logger = logging.getLogger(__name__)
INSTANCE_ID = os.getenv("INSTANCE_ID", "local")


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    get_engine()
    try:
        yield
    finally:
        dispose_database()


app = FastAPI(
    title="LAB01 Financial Event Processor",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(router)


@app.middleware("http")
async def identify_instance(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Instance-ID"] = INSTANCE_ID
    return response


@app.exception_handler(EventConflictError)
async def event_conflict_handler(_: Request, error: EventConflictError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(error)})


@app.exception_handler(EventValidationError)
async def event_validation_handler(_: Request, error: EventValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": str(error)})


@app.exception_handler(AccountNotFoundError)
async def account_not_found_handler(_: Request, error: AccountNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(error)})


@app.exception_handler(DatabaseConnectionError)
async def database_connection_handler(_: Request, error: DatabaseConnectionError) -> JSONResponse:
    logger.error("database_connection_failed error_type=%s", error.__class__.__name__)
    return JSONResponse(status_code=503, content={"detail": "Database unavailable"})


@app.exception_handler(QueryExecutionError)
async def query_execution_handler(_: Request, error: QueryExecutionError) -> JSONResponse:
    logger.error("database_query_failed error_type=%s", error.__class__.__name__)
    return JSONResponse(status_code=500, content={"detail": "Internal database error"})
