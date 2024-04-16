"""
Module of financial transactions' schemas
"""

from decimal import Decimal
from datetime import datetime
import enum
from typing import Annotated, Optional

from sqlalchemy import Enum, Numeric
from pydantic import (
    BaseModel,
    model_validator,
    Field,
    ConfigDict,
    UUID4,
)

from src.database.models import TrxType
from src.utils.as_form import as_form


@as_form
class FinancialTransactionModel(BaseModel):
    trx_type: TrxType
    debit: float
    credit: float
    user_id: UUID4 | int | None = None
    reservation_id: UUID4 | int

    @model_validator(mode="before")
    def round_debit_credit(cls, v):
        trx_type = v.get("trx_type")
        debit = v.get("debit")
        credit = v.get("credit")
        if trx_type == TrxType.CHARGE.value and credit != 0:
            raise ValueError(f"Charge transaction shouldn't has credit != 0")
        if trx_type == TrxType.PAYMENT.value and debit != 0:
            raise ValueError(f"Payment transaction shouldn't has debit != 0")
        v["debit"] = round(debit, 2)
        v["credit"] = round(credit, 2)
        return v


class FinancialTransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 | int
    trx_date: datetime
    trx_type: TrxType
    debit: float
    credit: float
    user_id: UUID4 | int | None = None
    reservation_id: UUID4 | int
