"""Verifica que invariantes de domínio também sejam impostas pelo PostgreSQL."""

from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.database.connection import get_engine


@pytest.mark.parametrize(
    ("operation", "amount", "currency", "status"),
    [
        ("TRANSFER", "1.00", "BRL", "RECEIVED"),
        ("CREDIT", "1.001", "BRL", "RECEIVED"),
        ("CREDIT", "1.00", "USD", "RECEIVED"),
        ("CREDIT", "1.00", "BRL", "UNKNOWN"),
    ],
)
def test_inbound_event_domain_checks(
    test_account_id: str,
    operation: str,
    amount: str,
    currency: str,
    status: str,
) -> None:
    with get_engine().connect() as connection:
        transaction = connection.begin()
        try:
            with pytest.raises(IntegrityError):
                with connection.begin_nested():
                    connection.execute(
                        text(
                            "INSERT INTO lab01.inbound_events "
                            "(event_id, account_id, operation, amount, currency, status_evento) "
                            "VALUES (:event_id, :account_id, :operation, :amount, :currency, :status)"
                        ),
                        {
                            "event_id": f"EVT-CHECK-{uuid4().hex}",
                            "account_id": test_account_id,
                            "operation": operation,
                            "amount": amount,
                            "currency": currency,
                            "status": status,
                        },
                    )
        finally:
            transaction.rollback()


def test_account_balance_rejects_fractional_cent(test_account_id: str) -> None:
    with get_engine().connect() as connection:
        transaction = connection.begin()
        try:
            with pytest.raises(IntegrityError):
                with connection.begin_nested():
                    connection.execute(
                        text(
                            "INSERT INTO lab01.accounts (account_id, saldo_atual) "
                            "VALUES (:account_id, 200.001)"
                        ),
                        {"account_id": f"{test_account_id}-BAD"},
                    )
        finally:
            transaction.rollback()


def test_transaction_must_match_inbound_event_business_values(test_account_id: str) -> None:
    event_id = f"EVT-MISMATCH-{uuid4().hex}"
    with get_engine().connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(
                text(
                    "INSERT INTO lab01.inbound_events "
                    "(event_id, account_id, operation, amount, currency, status_evento) "
                    "VALUES (:event_id, :account_id, 'CREDIT', 10.00, 'BRL', 'RECEIVED')"
                ),
                {"event_id": event_id, "account_id": test_account_id},
            )
            with pytest.raises(IntegrityError):
                with connection.begin_nested():
                    connection.execute(
                        text(
                            "INSERT INTO lab01.transactions "
                            "(account_id, event_id, valor, operacao, currency) "
                            "VALUES (:account_id, :event_id, 10.00, 'DEBIT', 'BRL')"
                        ),
                        {"event_id": event_id, "account_id": test_account_id},
                    )
        finally:
            transaction.rollback()
