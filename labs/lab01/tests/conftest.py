"""Fixtures compartilhadas dos testes de integração do LAB01."""

from collections.abc import Iterator
from uuid import uuid4

import pytest
from sqlalchemy import text

from src.database.connection import get_engine


@pytest.fixture
def test_account_id() -> Iterator[str]:
    account_id = f"TST-{uuid4().hex}"
    with get_engine().begin() as connection:
        connection.execute(
            text(
                "INSERT INTO lab01.accounts (account_id, saldo_atual) "
                "VALUES (:account_id, 200.00)"
            ),
            {"account_id": account_id},
        )

    try:
        yield account_id
    finally:
        with get_engine().begin() as connection:
            connection.execute(
                text("DELETE FROM lab01.transactions WHERE account_id = :account_id"),
                {"account_id": account_id},
            )
            connection.execute(
                text("DELETE FROM lab01.inbound_events WHERE account_id = :account_id"),
                {"account_id": account_id},
            )
            connection.execute(
                text("DELETE FROM lab01.accounts WHERE account_id = :account_id"),
                {"account_id": account_id},
            )
