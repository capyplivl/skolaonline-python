from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class PaymentStatus(StrEnum):
    NOT_PAID = "notPaid"
    PAID = "paid"
    PARTIALLY_PAID = "partiallyPaid"


class RegularPaymentsState(StrEnum):
    ALL = "all"
    PAID = "paid"
    PARTIALLY_PAID = "partiallyPaid"
    NOT_PAID = "notPaid"


@dataclass(kw_only=True)
class AllPayments(SkolaOnlineModel):
    payments: list[AllPaymentsItem] | None = None


@dataclass(kw_only=True)
class AllPaymentsItem(SkolaOnlineModel):
    payments_id: str
    title: str | None = None
    due_date: datetime | None = None
    amount: float | None = None
    original_amount: float | None = None
    status: PaymentStatus | None = None


@dataclass(kw_only=True)
class PaymentParentsNote(SkolaOnlineModel):
    parents_note: str | None = None


@dataclass(kw_only=True)
class PaymentsSummary(SkolaOnlineModel):
    paid: float | None = None
    amount_scheduled: float | None = None
    balance: float | None = None


@dataclass(kw_only=True)
class SinglePayment(SkolaOnlineModel):
    title: str | None = None
    due_date: datetime | None = None
    amount: float | None = None
    original_amount: float | None = None
    payment_status: PaymentStatus | None = None
    bank_account: str | None = None
    variable_symbol: str | None = None
    specific_symbol: str | None = None
    message: str | None = None
    payment_note: str | None = None
    parents_note: str | None = None
