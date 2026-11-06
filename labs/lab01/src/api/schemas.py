"""Contratos HTTP da API."""

from decimal import Decimal, InvalidOperation
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator


class EventRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: StrictStr = Field(min_length=1)
    account_id: StrictStr = Field(min_length=1)
    operation: Literal["CREDIT", "DEBIT"]
    amount: StrictStr
    currency: Literal["BRL"] = "BRL"

    @field_validator("event_id", "account_id")
    @classmethod
    def strip_identifiers(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Campo obrigatório não pode estar vazio.")
        return normalized

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: str) -> str:
        if re.fullmatch(r"[0-9]+(?:\.[0-9]{1,2})?", value) is None:
            raise ValueError("amount deve usar formato decimal simples com até duas casas.")
        try:
            amount = Decimal(value)
        except InvalidOperation as error:
            raise ValueError("amount deve ser uma string decimal.") from error
        if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
            raise ValueError("amount deve ser positivo e ter no máximo duas casas decimais.")
        return value


class EventResponse(BaseModel):
    event_id: str
    status: Literal["PROCESSED", "ALREADY_PROCESSED"]
    effect_applied: bool


class BalanceResponse(BaseModel):
    account_id: str
    balance: Decimal
    currency: Literal["BRL"] = "BRL"
