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
        """Return received messages matching the filter."""
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
        """Return a single received message."""
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
        """Return sent messages matching the filter."""
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
        """Return a single sent message."""
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
        """Return draft messages matching the filter."""
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
        """Return the settings for composing messages."""
        response = self._request("GET", "/api/v1/messages/settings")
        return parse_model(response, MessagesFormsResponse)

    def list_recipients(
        self, *, group_id: str | None = None, child_id: str | None = None
    ) -> Any:
        """Return one level of the available message recipients."""
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
        """Download an attachment of a message."""
        response = self._request(
            "GET",
            f"/api/v1/messages/{encode_path(message_id)}/attachments/{encode_path(attachment_id)}",
        )
        return downloaded_file(response)

    def send(self, body: MessageData) -> Any:
        """Send a message."""
        response = self._request("POST", "/api/v1/messages", json=body.to_dict())
        return parse_json(response)

    def send_draft(
        self, body: SendDraftMessageData, *, message_id: str | None = None
    ) -> Any:
        """Update a draft message with the given data and send it."""
        response = self._request(
            "POST",
            "/api/v1/teacher/messages/sendDraft",
            params={"messageId": message_id},
            json=body.to_dict(),
        )
        return parse_json(response)

    def create_draft(self, body: DraftMessageData) -> Any:
        """Save a new draft message."""
        response = self._request(
            "POST", "/api/v1/teacher/messages/draft", json=body.to_dict()
        )
        return parse_json(response)

    def vote(self, message_id: str, body: PostMessageVoteRequest) -> None:
        """Submit a vote answer for a poll message."""
        self._request(
            "POST",
            f"/api/v1/messages/{encode_path(message_id)}/vote",
            json=body.to_dict(),
        )

    def list_recipients_without_contacts(
        self, body: RecipientsWithoutContactsData
    ) -> Any:
        """Return recipients missing an email address or phone number."""
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
        """Attach a file to a message."""
        response = self._request(
            "POST",
            f"/api/v1/messages/{encode_path(message_id)}/attachments",
            params={"NameUser": display_name, "Name": name},
            files=[to_multipart("Data", file)],
        )
        return parse_json(response)

    def count_recipients(self, body: GetMessageRecipientsCountRequest) -> int:
        """Return the number of unique recipients for the given groups."""
        response = self._request(
            "POST", "/api/v1/messages/recipientsCount", json=body.to_dict()
        )
        return parse_int(response)

    def update_draft(self, message_id: str, body: UpdateMessageData) -> Any:
        """Update an unsent draft message."""
        response = self._request(
            "PUT",
            f"/api/v1/messages/{encode_path(message_id)}/draft",
            json=body.to_dict(),
        )
        return parse_json(response)

    def mark_as_read(self, message_id: str) -> None:
        """Mark a message as read."""
        self._request("PUT", f"/api/v1/messages/{encode_path(message_id)}/mark-as-read")

    def delete(self, message_id: str) -> Any:
        """Delete a message."""
        response = self._request(
            "DELETE", f"/api/v1/messages/{encode_path(message_id)}"
        )
        return parse_json(response)


class AsyncMessages(AsyncAPIResource):
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
        """Return received messages matching the filter."""
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
        """Return a single received message."""
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
        """Return sent messages matching the filter."""
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
        """Return a single sent message."""
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
        """Return draft messages matching the filter."""
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
        """Return the settings for composing messages."""
        response = await self._request("GET", "/api/v1/messages/settings")
        return parse_model(response, MessagesFormsResponse)

    async def list_recipients(
        self, *, group_id: str | None = None, child_id: str | None = None
    ) -> Any:
        """Return one level of the available message recipients."""
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
        """Download an attachment of a message."""
        response = await self._request(
            "GET",
            f"/api/v1/messages/{encode_path(message_id)}/attachments/{encode_path(attachment_id)}",
        )
        return downloaded_file(response)

    async def send(self, body: MessageData) -> Any:
        """Send a message."""
        response = await self._request("POST", "/api/v1/messages", json=body.to_dict())
        return parse_json(response)

    async def send_draft(
        self, body: SendDraftMessageData, *, message_id: str | None = None
    ) -> Any:
        """Update a draft message with the given data and send it."""
        response = await self._request(
            "POST",
            "/api/v1/teacher/messages/sendDraft",
            params={"messageId": message_id},
            json=body.to_dict(),
        )
        return parse_json(response)

    async def create_draft(self, body: DraftMessageData) -> Any:
        """Save a new draft message."""
        response = await self._request(
            "POST", "/api/v1/teacher/messages/draft", json=body.to_dict()
        )
        return parse_json(response)

    async def vote(self, message_id: str, body: PostMessageVoteRequest) -> None:
        """Submit a vote answer for a poll message."""
        await self._request(
            "POST",
            f"/api/v1/messages/{encode_path(message_id)}/vote",
            json=body.to_dict(),
        )

    async def list_recipients_without_contacts(
        self, body: RecipientsWithoutContactsData
    ) -> Any:
        """Return recipients missing an email address or phone number."""
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
        """Attach a file to a message."""
        response = await self._request(
            "POST",
            f"/api/v1/messages/{encode_path(message_id)}/attachments",
            params={"NameUser": display_name, "Name": name},
            files=[to_multipart("Data", file)],
        )
        return parse_json(response)

    async def count_recipients(self, body: GetMessageRecipientsCountRequest) -> int:
        """Return the number of unique recipients for the given groups."""
        response = await self._request(
            "POST", "/api/v1/messages/recipientsCount", json=body.to_dict()
        )
        return parse_int(response)

    async def update_draft(self, message_id: str, body: UpdateMessageData) -> Any:
        """Update an unsent draft message."""
        response = await self._request(
            "PUT",
            f"/api/v1/messages/{encode_path(message_id)}/draft",
            json=body.to_dict(),
        )
        return parse_json(response)

    async def mark_as_read(self, message_id: str) -> None:
        """Mark a message as read."""
        await self._request(
            "PUT", f"/api/v1/messages/{encode_path(message_id)}/mark-as-read"
        )

    async def delete(self, message_id: str) -> Any:
        """Delete a message."""
        response = await self._request(
            "DELETE", f"/api/v1/messages/{encode_path(message_id)}"
        )
        return parse_json(response)
