"""Rotas HTTP para processamento e consulta de contas."""

import logging

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from src.api.schemas import BalanceResponse, EventRequest, EventResponse
from src.database.connection import get_engine
from src.database.transaction import UnitOfWork
from src.repositories.accounts import AccountNotFoundError
from src.services.event_processor import EventProcessor

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health/live", tags=["health"])
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@router.get("/health/ready", tags=["health"])
def readiness() -> dict[str, str]:
    try:
        with get_engine().connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError as error:
        logger.warning("readiness_check_failed error_type=%s", error.__class__.__name__)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database is not ready",
        ) from error
    return {"status": "ready", "database": "ready"}


@router.post("/events", response_model=EventResponse, tags=["events"])
def process_event(payload: EventRequest) -> EventResponse:
    result = EventProcessor().process_event(payload.model_dump())
    logger.info(
        "event_processed event_id=%s status=%s",
        result["event_id"],
        result["status"],
    )
    return EventResponse(**result)


@router.get(
    "/accounts/{account_id}/balance",
    response_model=BalanceResponse,
    tags=["accounts"],
)
def get_account_balance(account_id: str) -> BalanceResponse:
    with UnitOfWork() as unit_of_work:
        balance = unit_of_work.accounts.get_by_account_id(account_id)
    if balance is None:
        raise AccountNotFoundError(f"Conta não encontrada: {account_id}")
    return BalanceResponse(account_id=account_id, balance=balance)
