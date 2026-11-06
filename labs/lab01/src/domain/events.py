"""Tipos e validações dos eventos financeiros."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


class EventValidationError(ValueError):
    """Evento inválido para processamento."""


class EventConflictError(ValueError):
    """Mesmo event_id recebido com conteúdo diferente."""


@dataclass(frozen=True)
class FinancialEvent:
    event_id: str
    account_id: str
    operation: str
    amount: Decimal
    currency: str = "BRL"

    @classmethod
    def from_payload(cls, payload: dict[str, object]) -> "FinancialEvent":
        try:
            amount = Decimal(str(payload["amount"]))
            event = cls(
                event_id=str(payload["event_id"]).strip(),
                account_id=str(payload["account_id"]).strip(),
                operation=str(payload["operation"]).strip().upper(),
                amount=amount,
                currency=str(payload.get("currency", "BRL")).strip().upper(),
            )
        except (KeyError, InvalidOperation, TypeError, ValueError) as error:
            raise EventValidationError("Payload do evento inválido.") from error
        event.validate()
        return event

    def validate(self) -> None:
        if not self.event_id or not self.account_id:
            raise EventValidationError("event_id e account_id são obrigatórios.")
        if self.operation not in {"CREDIT", "DEBIT"}:
            raise EventValidationError("operation deve ser CREDIT ou DEBIT.")
        if not self.amount.is_finite() or self.amount <= 0:
            raise EventValidationError("amount deve ser um valor decimal positivo e finito.")
        if self.amount.as_tuple().exponent < -2:
            raise EventValidationError("amount deve ter no máximo duas casas decimais.")
        if self.currency != "BRL":
            raise EventValidationError("Esta versão do laboratório aceita somente BRL.")

    @property
    def balance_delta(self) -> Decimal:
        return self.amount if self.operation == "CREDIT" else -self.amount
