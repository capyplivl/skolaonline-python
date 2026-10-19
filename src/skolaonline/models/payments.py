from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from skolaonline.models._base import SkolaOnlineModel


class PaymentStatus(StrEnum):
    """Payment state."""

    NOT_PAID = "notPaid"
    """Not paid."""

    PAID = "paid"
    """Paid."""

    PARTIALLY_PAID = "partiallyPaid"
    """Partially paid."""


class RegularPaymentsState(StrEnum):
    """Payment state filter."""

    ALL = "all"
    """All payments."""

    PAID = "paid"
    """Paid."""

    PARTIALLY_PAID = "partiallyPaid"
    """Partially paid."""

    NOT_PAID = "notPaid"
    """Not paid."""


@dataclass(kw_only=True)
class AllPayments(SkolaOnlineModel):
    """Regular payments of a student."""

    payments: list[AllPaymentsItem] | None = None
    """Payments."""


@dataclass(kw_only=True)
class AllPaymentsItem(SkolaOnlineModel):
    """Regular payment in a list."""

    payments_id: str
    """ID of the payment order."""

    title: str | None = None
    """Name of the payment."""

    due_date: datetime | None = None
    """Due date."""

    amount: float | None = None
    """Amount shown in the overview. The remaining amount for unpaid and partially
    paid orders, the ordered amount for paid ones."""

    original_amount: float | None = None
    """Ordered amount."""

    status: PaymentStatus | None = None
    """Payment state."""


@dataclass(kw_only=True)
class PaymentParentsNote(SkolaOnlineModel):
    """Note of a legal representative on a payment."""

    parents_note: str | None = None
    """Note of the legal representative."""


@dataclass(kw_only=True)
class PaymentsSummary(SkolaOnlineModel):
    """Summary of the regular payments of a student."""

    paid: float | None = None
    """Total amount paid."""

    amount_scheduled: float | None = None
    """Total amount ordered."""

    balance: float | None = None
    """Current balance."""


@dataclass(kw_only=True)
class SinglePayment(SkolaOnlineModel):
    """Payment order."""

    title: str | None = None
    """Name of the payment."""

    due_date: datetime | None = None
    """Due date."""

    amount: float | None = None
    """Amount shown in the overview. The remaining amount for unpaid and partially
    paid orders, the ordered amount for paid ones."""

    original_amount: float | None = None
    """Ordered amount."""

    payment_status: PaymentStatus | None = None
    """Payment state."""

    bank_account: str | None = None
    """Bank account."""

    variable_symbol: str | None = None
    """Variable symbol."""

    specific_symbol: str | None = None
    """Specific symbol."""

    message: str | None = None
    """Message for the recipient."""

    payment_note: str | None = None
    """Payment note."""

    parents_note: str | None = None
    """Note of the legal representative."""
