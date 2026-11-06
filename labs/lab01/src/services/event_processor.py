"""Caso de uso para processamento idempotente de eventos financeiros."""

from typing import Callable

from src.database.transaction import UnitOfWork
from src.domain.events import FinancialEvent
from src.services.ports import UnitOfWorkPort


class EventProcessor:
    def __init__(
        self,
        unit_of_work_factory: Callable[[], UnitOfWorkPort] = UnitOfWork,
    ) -> None:
        self._unit_of_work_factory = unit_of_work_factory

    def process_event(self, payload: dict[str, object] | FinancialEvent) -> dict[str, object]:
        event = payload if isinstance(payload, FinancialEvent) else FinancialEvent.from_payload(payload)
        event.validate()

        with self._unit_of_work_factory() as unit_of_work:
            unit_of_work.inbound_events.register_event(event)
            applied = unit_of_work.transactions.record_transaction(event)
            if applied:
                unit_of_work.accounts.update_balance(event.account_id, event.balance_delta)
            unit_of_work.inbound_events.mark_processed(event.event_id)

        return {
            "event_id": event.event_id,
            "status": "PROCESSED" if applied else "ALREADY_PROCESSED",
            "effect_applied": applied,
        }
