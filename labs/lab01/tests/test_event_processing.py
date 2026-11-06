"""Ensaios de aceitação de idempotência, atomicidade e concorrência."""

import json
import os
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from uuid import uuid4

import pytest
from sqlalchemy import text

from src.database.connection import get_engine
from src.domain.events import FinancialEvent
from src.repositories.accounts import AccountsRepository
from src.services.event_processor import EventProcessor

API_A = os.getenv("TEST_API_A_URL", "http://127.0.0.1:8001")
API_B = os.getenv("TEST_API_B_URL", "http://127.0.0.1:8002")


def post_event(base_url: str, payload: dict[str, str]) -> tuple[int, dict[str, object]]:
    request = Request(
        f"{base_url}/events",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=15) as response:
            return response.status, json.loads(response.read())
    except HTTPError as error:
        return error.code, json.loads(error.read())


def get_balance(base_url: str, account_id: str) -> Decimal:
    with urlopen(f"{base_url}/accounts/{account_id}/balance", timeout=10) as response:
        return Decimal(json.loads(response.read())["balance"])


def payload_for(account_id: str, event_id: str, operation: str, amount: str) -> dict[str, str]:
    return {
        "event_id": event_id,
        "account_id": account_id,
        "operation": operation,
        "amount": amount,
        "currency": "BRL",
    }


def test_t01_t02_t03_basic_scenario_and_redeliveries(test_account_id: str) -> None:
    suffix = uuid4().hex[:8]
    credit = payload_for(test_account_id, f"EVT-123-{suffix}", "CREDIT", "100.00")
    debit = payload_for(test_account_id, f"EVT-124-{suffix}", "DEBIT", "80.00")

    status_code, first = post_event(API_A, credit)
    assert status_code == 200
    assert first["effect_applied"] is True
    assert get_balance(API_A, test_account_id) == Decimal("300.00")

    for attempt in range(10):
        base_url = API_A if attempt % 2 == 0 else API_B
        status_code, duplicate = post_event(base_url, credit)
        assert status_code == 200
        assert duplicate["effect_applied"] is False
    assert get_balance(API_B, test_account_id) == Decimal("300.00")

    status_code, debit_result = post_event(API_B, debit)
    assert status_code == 200
    assert debit_result["effect_applied"] is True
    assert get_balance(API_A, test_account_id) == Decimal("220.00")


def test_t04_two_workers_apply_same_event_once(test_account_id: str) -> None:
    payload = payload_for(test_account_id, f"EVT-125-{uuid4().hex[:8]}", "CREDIT", "100.00")
    with ThreadPoolExecutor(max_workers=2) as workers:
        results = list(workers.map(lambda url: post_event(url, payload), [API_A, API_B]))

    assert [status for status, _ in results] == [200, 200]
    assert sum(bool(result["effect_applied"]) for _, result in results) == 1
    assert get_balance(API_A, test_account_id) == Decimal("300.00")


def test_t05_failure_before_commit_rolls_back_all_changes(
    test_account_id: str,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    event_id = f"EVT-FAIL-{uuid4().hex[:8]}"
    event = FinancialEvent(
        event_id=event_id,
        account_id=test_account_id,
        operation="CREDIT",
        amount=Decimal("25.00"),
    )

    def fail_balance_update(*_: object, **__: object) -> Decimal:
        raise RuntimeError("injected pre-commit failure")

    monkeypatch.setattr(AccountsRepository, "update_balance", fail_balance_update)
    with pytest.raises(RuntimeError, match="injected pre-commit failure"):
        EventProcessor().process_event(event)

    with get_engine().connect() as connection:
        event_count = connection.execute(
            text("SELECT count(*) FROM lab01.inbound_events WHERE event_id = :event_id"),
            {"event_id": event_id},
        ).scalar_one()
        transaction_count = connection.execute(
            text("SELECT count(*) FROM lab01.transactions WHERE event_id = :event_id"),
            {"event_id": event_id},
        ).scalar_one()
    assert event_count == 0
    assert transaction_count == 0
    assert get_balance(API_A, test_account_id) == Decimal("200.00")


def test_t06_retry_after_commit_does_not_apply_effect_again(test_account_id: str) -> None:
    payload = payload_for(test_account_id, f"EVT-ACK-{uuid4().hex[:8]}", "CREDIT", "35.00")

    # Ignore the first successful response to simulate a lost acknowledgement.
    first_status, _ = post_event(API_A, payload)
    assert first_status == 200
    retry_status, retry = post_event(API_B, payload)

    assert retry_status == 200
    assert retry["effect_applied"] is False
    assert get_balance(API_A, test_account_id) == Decimal("235.00")


def test_t07_distinct_parallel_events_do_not_lose_balance_updates(test_account_id: str) -> None:
    suffix = uuid4().hex[:8]
    events = [
        payload_for(test_account_id, f"EVT-PAR-A-{suffix}", "CREDIT", "10.00"),
        payload_for(test_account_id, f"EVT-PAR-B-{suffix}", "CREDIT", "20.00"),
    ]
    with ThreadPoolExecutor(max_workers=2) as workers:
        results = list(workers.map(post_event, [API_A, API_B], events))

    assert [status for status, _ in results] == [200, 200]
    assert all(result["effect_applied"] is True for _, result in results)
    assert get_balance(API_A, test_account_id) == Decimal("230.00")
