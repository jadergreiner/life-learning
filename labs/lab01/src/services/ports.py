"""Contratos usados pelo caso de uso sem dependência do driver SQL."""

from decimal import Decimal
from types import TracebackType
from typing import Protocol, Self

from src.domain.events import FinancialEvent


class AccountsPort(Protocol):
    def update_balance(self, account_id: str, amount_delta: Decimal) -> Decimal: ...


class InboundEventsPort(Protocol):
    def register_event(self, event: FinancialEvent) -> bool: ...

    def mark_processed(self, event_id: str) -> None: ...


class TransactionsPort(Protocol):
    def record_transaction(self, event: FinancialEvent) -> bool: ...


class UnitOfWorkPort(Protocol):
    accounts: AccountsPort
    inbound_events: InboundEventsPort
    transactions: TransactionsPort

    def __enter__(self) -> Self: ...

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None: ...
