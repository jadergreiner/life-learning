"""Persistência de eventos recebidos."""

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.events import EventConflictError, FinancialEvent


class InboundEventsRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def register_event(self, event: FinancialEvent) -> bool:
        inserted = self._session.execute(
            text(
                "INSERT INTO lab01.inbound_events "
                "(event_id, account_id, operation, amount, currency, status_evento) "
                "VALUES (:event_id, :account_id, :operation, :amount, :currency, 'RECEIVED') "
                "ON CONFLICT DO NOTHING "
                "RETURNING event_id"
            ),
            {
                "event_id": event.event_id,
                "account_id": event.account_id,
                "operation": event.operation,
                "amount": event.amount,
                "currency": event.currency,
            },
        ).scalar_one_or_none()

        if inserted is not None:
            return True

        existing = self._session.execute(
            text(
                "SELECT account_id, operation, amount, currency "
                "FROM lab01.inbound_events WHERE event_id = :event_id"
            ),
            {"event_id": event.event_id},
        ).mappings().one()
        expected = (event.account_id, event.operation, event.amount, event.currency)
        actual = (
            existing["account_id"],
            existing["operation"],
            existing["amount"],
            existing["currency"],
        )
        if actual != expected:
            raise EventConflictError(
                f"event_id {event.event_id} já foi recebido com conteúdo diferente."
            )
        return False

    def mark_processed(self, event_id: str) -> None:
        self._session.execute(
            text(
                "UPDATE lab01.inbound_events SET status_evento = 'PROCESSED' "
                "WHERE event_id = :event_id"
            ),
            {"event_id": event_id},
        )
