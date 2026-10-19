from __future__ import annotations

from collections.abc import Sequence

from skolaonline.models import (
    AllPayments,
    PaymentParentsNote,
    PaymentsSummary,
    RegularPaymentsState,
    SinglePayment,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    encode_path,
    parse_model,
)


class Payments(SyncAPIResource):
    """Endpoints for payments of students."""

    def retrieve_summary(self, student_id: str) -> PaymentsSummary:
        """Return the summary of regular payments of a student.

        Args:
            student_id: ID of the student.

        Returns:
            Summary of the regular payments of a student.
        """
        response = self._request(
            "GET",
            f"/api/v1/student/{encode_path(student_id)}/payments/regularpayments/summary",
        )
        return parse_model(response, PaymentsSummary)

    def list_regular(
        self,
        student_id: str,
        *,
        state: Sequence[RegularPaymentsState] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> AllPayments:
        """Return regular payments of a student.

        Args:
            student_id: ID of the student.
            state: Payment states to return.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Regular payments of a student.
        """
        response = self._request(
            "GET",
            f"/api/v1/student/{encode_path(student_id)}/payments/regularpayments",
            params={
                "State": state,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, AllPayments)

    def retrieve(self, payment_id: str) -> SinglePayment:
        """Return a single payment.

        Args:
            payment_id: ID of the payment order.

        Returns:
            Payment order.
        """
        response = self._request(
            "GET", f"/api/v1/student/payments/{encode_path(payment_id)}"
        )
        return parse_model(response, SinglePayment)

    def update_parents_note(
        self, payment_id: str, body: PaymentParentsNote
    ) -> PaymentParentsNote:
        """Update the parents note of a payment.

        Args:
            payment_id: ID of the payment order.
            body: Note of the legal representative.

        Returns:
            Note of a legal representative on a payment.
        """
        response = self._request(
            "PUT",
            f"/api/v1/student/payments/{encode_path(payment_id)}",
            json=body.to_dict(),
        )
        return parse_model(response, PaymentParentsNote)


class AsyncPayments(AsyncAPIResource):
    """Asynchronous endpoints for payments of students."""

    async def retrieve_summary(self, student_id: str) -> PaymentsSummary:
        """Return the summary of regular payments of a student.

        Args:
            student_id: ID of the student.

        Returns:
            Summary of the regular payments of a student.
        """
        response = await self._request(
            "GET",
            f"/api/v1/student/{encode_path(student_id)}/payments/regularpayments/summary",
        )
        return parse_model(response, PaymentsSummary)

    async def list_regular(
        self,
        student_id: str,
        *,
        state: Sequence[RegularPaymentsState] | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> AllPayments:
        """Return regular payments of a student.

        Args:
            student_id: ID of the student.
            state: Payment states to return.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Regular payments of a student.
        """
        response = await self._request(
            "GET",
            f"/api/v1/student/{encode_path(student_id)}/payments/regularpayments",
            params={
                "State": state,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, AllPayments)

    async def retrieve(self, payment_id: str) -> SinglePayment:
        """Return a single payment.

        Args:
            payment_id: ID of the payment order.

        Returns:
            Payment order.
        """
        response = await self._request(
            "GET", f"/api/v1/student/payments/{encode_path(payment_id)}"
        )
        return parse_model(response, SinglePayment)

    async def update_parents_note(
        self, payment_id: str, body: PaymentParentsNote
    ) -> PaymentParentsNote:
        """Update the parents note of a payment.

        Args:
            payment_id: ID of the payment order.
            body: Note of the legal representative.

        Returns:
            Note of a legal representative on a payment.
        """
        response = await self._request(
            "PUT",
            f"/api/v1/student/payments/{encode_path(payment_id)}",
            json=body.to_dict(),
        )
        return parse_model(response, PaymentParentsNote)
