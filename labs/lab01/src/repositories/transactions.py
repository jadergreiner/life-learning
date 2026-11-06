"""Registro imutável dos efeitos financeiros aplicados."""

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.events import FinancialEvent


class TransactionsRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def record_transaction(self, event: FinancialEvent) -> bool:
        inserted = self._session.execute(
            text(
                "INSERT INTO lab01.transactions "
                "(account_id, event_id, valor, operacao, currency) "
                "VALUES (:account_id, :event_id, :amount, :operation, :currency) "
                "ON CONFLICT (event_id) DO NOTHING "
                "RETURNING event_id"
            ),
            {
                "account_id": event.account_id,
                "event_id": event.event_id,
                "amount": event.amount,
                "operation": event.operation,
                "currency": event.currency,
            },
        ).scalar_one_or_none()
        return inserted is not None

    def exists_by_event_id(self, event_id: str) -> bool:
        return bool(
            self._session.execute(
                text(
                    "SELECT EXISTS (SELECT 1 FROM lab01.transactions "
                    "WHERE event_id = :event_id)"
                ),
                {"event_id": event_id},
            ).scalar_one()
        )
