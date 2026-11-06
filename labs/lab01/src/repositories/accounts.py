"""Consultas e atualizações da tabela de contas."""

from decimal import Decimal

from sqlalchemy import text
from sqlalchemy.orm import Session


class AccountNotFoundError(LookupError):
    """A conta informada não existe."""


class AccountsRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_account_id(self, account_id: str) -> Decimal | None:
        result = self._session.execute(
            text("SELECT saldo_atual FROM lab01.accounts WHERE account_id = :account_id"),
            {"account_id": account_id},
        ).scalar_one_or_none()
        return result

    def update_balance(self, account_id: str, amount_delta: Decimal) -> Decimal:
        result = self._session.execute(
            text(
                "UPDATE lab01.accounts "
                "SET saldo_atual = saldo_atual + :amount_delta "
                "WHERE account_id = :account_id "
                "RETURNING saldo_atual"
            ),
            {"account_id": account_id, "amount_delta": amount_delta},
        ).scalar_one_or_none()
        if result is None:
            raise AccountNotFoundError(f"Conta não encontrada: {account_id}")
        return result
