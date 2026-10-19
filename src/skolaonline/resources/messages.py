from __future__ import annotations

from typing import Any

from skolaonline._files import DownloadedFile, downloaded_file, to_multipart
from skolaonline._types import DateLike, FileInput
from skolaonline.models import (
    ConceptMessageOrder,
    ConceptMessagesResponse,
    DraftMessageData,
    GetMessageRecipientsCountRequest,
    MessageData,
    MessageOrder,
    MessageReadStatus,
    MessagesFormsResponse,
    PostMessageVoteRequest,
    ReceivedMessage,
    ReceivedMessagesResponse,
    RecipientsWithoutContactsData,
    SendDraftMessageData,
    SenderPersonType,
    SentMessagesResponse,
    UpdateMessageData,
)
from skolaonline.resources._base import (
    AsyncAPIResource,
    SyncAPIResource,
    encode_path,
    parse_int,
    parse_json,
    parse_model,
)


class Messages(SyncAPIResource):
    """Endpoints for messages."""

    def list_received(
        self,
        *,
        sender_person_type: SenderPersonType | None = None,
        message_read_status: MessageReadStatus | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        order_by: MessageOrder | None = None,
        search: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> ReceivedMessagesResponse:
        """Return received messages matching the filter.

        Args:
            sender_person_type: Type of the sender.
            message_read_status: Filter by read state.
            date_from: Return messages sent on or after this date.
            date_to: Return messages sent on or before this date.
            order_by: Sort order. Defaults to newest first.
            search: Full-text search.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Received messages.
        """
        response = self._request(
            "GET",
            "/api/v1/messages/received",
            params={
                "SenderPersonType": sender_person_type,
                "MessageReadStatus": message_read_status,
                "DateFrom": date_from,
                "DateTo": date_to,
                "OrderBy": order_by,
                "Search": search,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, ReceivedMessagesResponse)

    def retrieve_received(self, message_id: str) -> ReceivedMessage:
        """Return a single received message.

        Args:
            message_id: ID of the message.

        Returns:
            Received message.
        """
        response = self._request(
            "GET", f"/api/v1/messages/received/{encode_path(message_id)}"
        )
        return parse_model(response, ReceivedMessage)

    def list_sent(
        self,
        *,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        order_by: MessageOrder | None = None,
        search: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> SentMessagesResponse:
        """Return sent messages matching the filter.

        Args:
            date_from: Return messages sent on or after this date.
            date_to: Return messages sent on or before this date.
            order_by: Sort order. Defaults to newest first.
            search: Full-text search.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Sent messages.
        """
        response = self._request(
            "GET",
            "/api/v1/messages/sent",
            params={
                "DateFrom": date_from,
                "DateTo": date_to,
                "OrderBy": order_by,
                "Search": search,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, SentMessagesResponse)

    def retrieve_sent(self, message_id: str) -> Any:
        """Return a single sent message.

        Args:
            message_id: ID of the message.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "GET", f"/api/v1/messages/sent/{encode_path(message_id)}"
        )
        return parse_json(response)

    def list_drafts(
        self,
        *,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        order_by: ConceptMessageOrder | None = None,
        search: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> ConceptMessagesResponse:
        """Return draft messages matching the filter.

        Args:
            date_from: Return drafts saved on or after this date. Defaults to the start
                of the school year.
            date_to: Return drafts saved on or before this date. Defaults to the end of
                the school year.
            order_by: Sort order of draft messages. Defaults to newest first.
            search: Full-text search.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Draft messages.
        """
        response = self._request(
            "GET",
            "/api/v1/messages/draft",
            params={
                "DateFrom": date_from,
                "DateTo": date_to,
                "OrderBy": order_by,
                "Search": search,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, ConceptMessagesResponse)

    def retrieve_settings(self) -> MessagesFormsResponse:
        """Return the settings for composing messages.

        Returns:
            Settings for composing messages.
        """
        response = self._request("GET", "/api/v1/messages/settings")
        return parse_model(response, MessagesFormsResponse)

    def list_recipients(
        self, *, group_id: str | None = None, child_id: str | None = None
    ) -> Any:
        """Return one level of the available message recipients.

        Args:
            group_id: ID of the recipient level to expand. The top level is returned
                when omitted, for example the teachers for parents or the standard
                recipient groups for employees.
            child_id: ID of the child. Used by parents.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "GET",
            "/api/v1/messages/recipients",
            params={"id": group_id},
            headers={"api-ChildId": child_id},
        )
        return parse_json(response)

    def download_attachment(
        self, message_id: str, attachment_id: str
    ) -> DownloadedFile:
        """Download an attachment of a message.

        Args:
            message_id: ID of the message.
            attachment_id: ID of the attachment.

        Returns:
            Downloaded file with its name and content type.
        """
        response = self._request(
            "GET",
            f"/api/v1/messages/{encode_path(message_id)}/attachments/{encode_path(attachment_id)}",
        )
        return downloaded_file(response)

    def send(self, body: MessageData) -> Any:
        """Send a message.

        Args:
            body: Message to send.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request("POST", "/api/v1/messages", json=body.to_dict())
        return parse_json(response)

    def send_draft(
        self, body: SendDraftMessageData, *, message_id: str | None = None
    ) -> Any:
        """Update a draft message with the given data and send it.

        Args:
            body: Message to send.
            message_id: ID of the draft message.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "POST",
            "/api/v1/teacher/messages/sendDraft",
            params={"messageId": message_id},
            json=body.to_dict(),
        )
        return parse_json(response)

    def create_draft(self, body: DraftMessageData) -> Any:
        """Save a new draft message.

        Args:
            body: Draft message to save.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "POST", "/api/v1/teacher/messages/draft", json=body.to_dict()
        )
        return parse_json(response)

    def vote(self, message_id: str, body: PostMessageVoteRequest) -> None:
        """Submit a vote answer for a poll message.

        Args:
            message_id: ID of the poll message.
            body: Vote answer.
        """
        self._request(
            "POST",
            f"/api/v1/messages/{encode_path(message_id)}/vote",
            json=body.to_dict(),
        )

    def list_recipients_without_contacts(
        self, body: RecipientsWithoutContactsData
    ) -> Any:
        """Return recipients missing an email address or phone number.

        Args:
            body: Recipients and the requested form of delivery.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "POST", "/api/v1/messages/withoutcontacts", json=body.to_dict()
        )
        return parse_json(response)

    def upload_attachment(
        self,
        message_id: str,
        file: FileInput,
        *,
        name: str,
        display_name: str | None = None,
    ) -> Any:
        """Attach a file to a message.

        Args:
            message_id: ID of the message.
            file: File to attach.
            name: Physical name of the file.
            display_name: File name shown to users.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "POST",
            f"/api/v1/messages/{encode_path(message_id)}/attachments",
            params={"NameUser": display_name, "Name": name},
            files=[to_multipart("Data", file)],
        )
        return parse_json(response)

    def count_recipients(self, body: GetMessageRecipientsCountRequest) -> int:
        """Return the number of unique recipients for the given groups.

        Args:
            body: Recipient groups to count.

        Returns:
            Number of unique recipients.
        """
        response = self._request(
            "POST", "/api/v1/messages/recipientsCount", json=body.to_dict()
        )
        return parse_int(response)

    def update_draft(self, message_id: str, body: UpdateMessageData) -> Any:
        """Update an unsent draft message.

        Args:
            message_id: ID of the draft message to update.
            body: Updated data of the draft message.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "PUT",
            f"/api/v1/messages/{encode_path(message_id)}/draft",
            json=body.to_dict(),
        )
        return parse_json(response)

    def mark_as_read(self, message_id: str) -> None:
        """Mark a message as read.

        Args:
            message_id: ID of the message to mark as read.
        """
        self._request("PUT", f"/api/v1/messages/{encode_path(message_id)}/mark-as-read")

    def delete(self, message_id: str) -> Any:
        """Delete a message.

        Args:
            message_id: ID of the message to delete.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = self._request(
            "DELETE", f"/api/v1/messages/{encode_path(message_id)}"
        )
        return parse_json(response)


class AsyncMessages(AsyncAPIResource):
    """Asynchronous endpoints for messages."""

    async def list_received(
        self,
        *,
        sender_person_type: SenderPersonType | None = None,
        message_read_status: MessageReadStatus | None = None,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        order_by: MessageOrder | None = None,
        search: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> ReceivedMessagesResponse:
        """Return received messages matching the filter.

        Args:
            sender_person_type: Type of the sender.
            message_read_status: Filter by read state.
            date_from: Return messages sent on or after this date.
            date_to: Return messages sent on or before this date.
            order_by: Sort order. Defaults to newest first.
            search: Full-text search.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Received messages.
        """
        response = await self._request(
            "GET",
            "/api/v1/messages/received",
            params={
                "SenderPersonType": sender_person_type,
                "MessageReadStatus": message_read_status,
                "DateFrom": date_from,
                "DateTo": date_to,
                "OrderBy": order_by,
                "Search": search,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, ReceivedMessagesResponse)

    async def retrieve_received(self, message_id: str) -> ReceivedMessage:
        """Return a single received message.

        Args:
            message_id: ID of the message.

        Returns:
            Received message.
        """
        response = await self._request(
            "GET", f"/api/v1/messages/received/{encode_path(message_id)}"
        )
        return parse_model(response, ReceivedMessage)

    async def list_sent(
        self,
        *,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        order_by: MessageOrder | None = None,
        search: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> SentMessagesResponse:
        """Return sent messages matching the filter.

        Args:
            date_from: Return messages sent on or after this date.
            date_to: Return messages sent on or before this date.
            order_by: Sort order. Defaults to newest first.
            search: Full-text search.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Sent messages.
        """
        response = await self._request(
            "GET",
            "/api/v1/messages/sent",
            params={
                "DateFrom": date_from,
                "DateTo": date_to,
                "OrderBy": order_by,
                "Search": search,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, SentMessagesResponse)

    async def retrieve_sent(self, message_id: str) -> Any:
        """Return a single sent message.

        Args:
            message_id: ID of the message.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "GET", f"/api/v1/messages/sent/{encode_path(message_id)}"
        )
        return parse_json(response)

    async def list_drafts(
        self,
        *,
        date_from: DateLike | None = None,
        date_to: DateLike | None = None,
        order_by: ConceptMessageOrder | None = None,
        search: str | None = None,
        page_number: int | None = None,
        page_size: int | None = None,
    ) -> ConceptMessagesResponse:
        """Return draft messages matching the filter.

        Args:
            date_from: Return drafts saved on or after this date. Defaults to the start
                of the school year.
            date_to: Return drafts saved on or before this date. Defaults to the end of
                the school year.
            order_by: Sort order of draft messages. Defaults to newest first.
            search: Full-text search.
            page_number: Page number, starting at 1.
            page_size: Page size.

        Returns:
            Draft messages.
        """
        response = await self._request(
            "GET",
            "/api/v1/messages/draft",
            params={
                "DateFrom": date_from,
                "DateTo": date_to,
                "OrderBy": order_by,
                "Search": search,
                "Pagination.PageNumber": page_number,
                "Pagination.PageSize": page_size,
            },
        )
        return parse_model(response, ConceptMessagesResponse)

    async def retrieve_settings(self) -> MessagesFormsResponse:
        """Return the settings for composing messages.

        Returns:
            Settings for composing messages.
        """
        response = await self._request("GET", "/api/v1/messages/settings")
        return parse_model(response, MessagesFormsResponse)

    async def list_recipients(
        self, *, group_id: str | None = None, child_id: str | None = None
    ) -> Any:
        """Return one level of the available message recipients.

        Args:
            group_id: ID of the recipient level to expand. The top level is returned
                when omitted, for example the teachers for parents or the standard
                recipient groups for employees.
            child_id: ID of the child. Used by parents.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "GET",
            "/api/v1/messages/recipients",
            params={"id": group_id},
            headers={"api-ChildId": child_id},
        )
        return parse_json(response)

    async def download_attachment(
        self, message_id: str, attachment_id: str
    ) -> DownloadedFile:
        """Download an attachment of a message.

        Args:
            message_id: ID of the message.
            attachment_id: ID of the attachment.

        Returns:
            Downloaded file with its name and content type.
        """
        response = await self._request(
            "GET",
            f"/api/v1/messages/{encode_path(message_id)}/attachments/{encode_path(attachment_id)}",
        )
        return downloaded_file(response)

    async def send(self, body: MessageData) -> Any:
        """Send a message.

        Args:
            body: Message to send.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request("POST", "/api/v1/messages", json=body.to_dict())
        return parse_json(response)

    async def send_draft(
        self, body: SendDraftMessageData, *, message_id: str | None = None
    ) -> Any:
        """Update a draft message with the given data and send it.

        Args:
            body: Message to send.
            message_id: ID of the draft message.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "POST",
            "/api/v1/teacher/messages/sendDraft",
            params={"messageId": message_id},
            json=body.to_dict(),
        )
        return parse_json(response)

    async def create_draft(self, body: DraftMessageData) -> Any:
        """Save a new draft message.

        Args:
            body: Draft message to save.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "POST", "/api/v1/teacher/messages/draft", json=body.to_dict()
        )
        return parse_json(response)

    async def vote(self, message_id: str, body: PostMessageVoteRequest) -> None:
        """Submit a vote answer for a poll message.

        Args:
            message_id: ID of the poll message.
            body: Vote answer.
        """
        await self._request(
            "POST",
            f"/api/v1/messages/{encode_path(message_id)}/vote",
            json=body.to_dict(),
        )

    async def list_recipients_without_contacts(
        self, body: RecipientsWithoutContactsData
    ) -> Any:
        """Return recipients missing an email address or phone number.

        Args:
            body: Recipients and the requested form of delivery.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "POST", "/api/v1/messages/withoutcontacts", json=body.to_dict()
        )
        return parse_json(response)

    async def upload_attachment(
        self,
        message_id: str,
        file: FileInput,
        *,
        name: str,
        display_name: str | None = None,
    ) -> Any:
        """Attach a file to a message.

        Args:
            message_id: ID of the message.
            file: File to attach.
            name: Physical name of the file.
            display_name: File name shown to users.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "POST",
            f"/api/v1/messages/{encode_path(message_id)}/attachments",
            params={"NameUser": display_name, "Name": name},
            files=[to_multipart("Data", file)],
        )
        return parse_json(response)

    async def count_recipients(self, body: GetMessageRecipientsCountRequest) -> int:
        """Return the number of unique recipients for the given groups.

        Args:
            body: Recipient groups to count.

        Returns:
            Number of unique recipients.
        """
        response = await self._request(
            "POST", "/api/v1/messages/recipientsCount", json=body.to_dict()
        )
        return parse_int(response)

    async def update_draft(self, message_id: str, body: UpdateMessageData) -> Any:
        """Update an unsent draft message.

        Args:
            message_id: ID of the draft message to update.
            body: Updated data of the draft message.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "PUT",
            f"/api/v1/messages/{encode_path(message_id)}/draft",
            json=body.to_dict(),
        )
        return parse_json(response)

    async def mark_as_read(self, message_id: str) -> None:
        """Mark a message as read.

        Args:
            message_id: ID of the message to mark as read.
        """
        await self._request(
            "PUT", f"/api/v1/messages/{encode_path(message_id)}/mark-as-read"
        )

    async def delete(self, message_id: str) -> Any:
        """Delete a message.

        Args:
            message_id: ID of the message to delete.

        Returns:
            Decoded JSON response, or None when the response is empty.
        """
        response = await self._request(
            "DELETE", f"/api/v1/messages/{encode_path(message_id)}"
        )
        return parse_json(response)
