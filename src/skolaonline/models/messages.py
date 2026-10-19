from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import UserType
from skolaonline.models.user import UserChild


class AvatarIcon(StrEnum):
    """Icon representing a person."""

    STUDENT = "student"
    """Student."""

    STUDENT_AND_PARENT = "studentAndParent"
    """Student and parent."""

    PARENT = "parent"
    """Parent."""

    PRIMARY_PARENT = "primaryParent"
    """Primary parent."""

    EMPLOYEE = "employee"
    """Employee."""


class ConceptMessageOrder(StrEnum):
    """Sort order of draft messages. Defaults to newest first."""

    DATE_SAVE_DESC = "dateSaveDesc"
    """By save date, newest first."""

    DATE_SAVE_ASC = "dateSaveAsc"
    """By save date, oldest first."""


class FormOfDelivery(StrEnum):
    """Requested form of delivery."""

    MAILSMS = "mailsms"
    """Email and text message."""

    MAIL = "mail"
    """Email."""

    SMS = "sms"
    """Text message."""


class MessageOrder(StrEnum):
    """Sort order of messages. Defaults to newest first."""

    DATE_SEND_DESC = "dateSendDesc"
    """By send date, newest first."""

    DATE_SEND_ASC = "dateSendAsc"
    """By send date, oldest first."""


class MessageReadStatus(StrEnum):
    """Filter of messages by read state."""

    NOT_RESTRICTED = "notRestricted"
    """Read and unread messages."""

    READ = "read"
    """Read messages only."""

    NOT_READ = "notRead"
    """Unread messages only."""


class SenderPersonType(StrEnum):
    """Filter of received messages by sender type."""

    NOT_RESTRICTED = "notRestricted"
    """Any sender."""

    STUDENT = "student"
    """Students."""

    PARENT = "parent"
    """Parents."""

    EMPLOYEE = "employee"
    """Employees."""


class SendingType(StrEnum):
    """Way a message was sent."""

    SMS = "sms"
    """Text message."""

    EMAIL = "email"
    """Email."""

    SYSTEM_MESSAGE = "systemMessage"
    """In-app message."""

    SYSTEM_MESSAGE_WITH_VOTE = "systemMessageWithVote"
    """In-app message with a poll."""


@dataclass(kw_only=True)
class ConceptMessage(SkolaOnlineModel):
    """Draft message."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    id: str
    """ID of the message."""

    title: str | None = None
    """Subject of the message."""

    text: str | None = None
    """Message text in HTML."""

    save_date: datetime
    """Date the draft was saved."""

    recipients: list[RelevantPerson]
    """Recipients of the message."""

    attachments_delete_date: datetime | None = None
    """Date the attachments will be deleted."""

    attachments_delete_text: str | None = None
    """Text shown in the message detail after the attachments are deleted from
    storage."""

    vote_options: list[str]
    """Voting options."""

    attachments: list[MessageAttachment]
    """Attachments of the message."""

    send_as_email: bool
    """Whether the message is sent as an email."""

    send_as_sms: bool
    """Whether the message is sent as a text message."""

    send_as_system_message: bool
    """Whether the message is sent as an in-app message."""

    sender_of_email: str | None = None
    """Sender of the email."""

    previous_message_id: str | None = None
    """ID of the received message this draft replies to."""


@dataclass(kw_only=True)
class ConceptMessagesResponse(SkolaOnlineModel):
    """Draft messages."""

    message: str | None = None
    """Warning for the user when a non-essential part of the operation failed."""

    messages: list[ConceptMessage]
    """Messages."""


@dataclass(kw_only=True)
class DraftMessageData(SkolaOnlineModel):
    """Data of a new draft message."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    previous_message_id: str | None = None
    """ID of the previous message. Only set when replying to a message."""

    attachments: list[str]
    """IDs of attached files. Upload the files before sending the message."""

    send_as_email: bool
    """Whether to send the message as an email."""

    send_as_sms: bool
    """Whether to send the message as a text message."""

    send_as_system_message: bool
    """Whether to send the message as an in-app message."""

    sender_of_email: str | None = None
    """Email address used as the sender of emails. The value self uses the address of
    the recipient."""

    attachments_delete_date: datetime | None = None
    """Date the attachments will be deleted, set by the sender."""

    vote_options: list[str]
    """Voting options."""

    title: str | None = None
    """Subject of the message."""

    text: str | None = None
    """Message text."""

    recipients: list[str]
    """IDs of the recipients."""


@dataclass(kw_only=True)
class GetMessageRecipientsCountRequest(SkolaOnlineModel):
    """Recipient groups to count."""

    recipients_groups: list[str]
    """IDs of the recipient groups."""


@dataclass(kw_only=True)
class MessageAttachment(SkolaOnlineModel):
    """Attachment of a message."""

    id: str
    """ID used to download the file."""

    name: str
    """Physical file name."""

    name_user: str | None = None
    """File name shown to users."""

    type: str | None = None
    """File type."""

    size: int
    """File size in bytes."""


@dataclass(kw_only=True)
class MessageData(SkolaOnlineModel):
    """Data of a new message."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    title: str
    """Subject of the message."""

    text: str
    """Message text."""

    recipients: list[str]
    """IDs of the recipients."""

    previous_message_id: str | None = None
    """ID of the previous message. Only set when replying to a message."""

    attachments: list[str]
    """IDs of attached files. Upload the files before sending the message."""

    send_as_email: bool
    """Whether to send the message as an email."""

    send_as_sms: bool
    """Whether to send the message as a text message."""

    send_as_system_message: bool
    """Whether to send the message as an in-app message."""

    sender_of_email: str | None = None
    """Email address used as the sender of emails. The value self uses the address of
    the recipient."""

    attachments_delete_date: datetime | None = None
    """Date the attachments will be deleted, set by the sender."""

    vote_options: list[str]
    """Voting options."""


@dataclass(kw_only=True)
class MessagesFormsResponse(SkolaOnlineModel):
    """Settings for composing messages."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "implicit_sms": "implicitSMS",
    }

    system_message: bool
    """Whether the user can send in-app messages."""

    email: bool
    """Whether the user can send emails."""

    sender_of_email: list[str]
    """Email addresses usable as the sender, ordered by priority: personal or school
    email, then the email of the organization. Contains self when no address is
    registered, meaning the address of the recipient is used."""

    sms: bool
    """Whether the user can send text messages."""

    attachment: bool
    """Whether the user can attach files. Currently only internal users sending
    emails."""

    implicit_system_message: bool
    """Whether new messages are sent in the app by default."""

    implicit_email: bool
    """Whether new messages are sent as emails by default."""

    implicit_sms: bool
    """Whether new messages are sent as text messages by default."""

    alert_number_of_recipients: int | None = None
    """Number of recipients that triggers a warning. Null disables the check."""

    list_of_voting_options: list[list[str]]
    """Voting options for poll messages."""

    max_attachment_size: int | None = None
    """Maximum total size of message attachments in bytes."""


@dataclass(kw_only=True)
class PostMessageVoteRequest(SkolaOnlineModel):
    """Vote answer for a poll message."""

    vote_answer: str | None = None
    """Selected answer."""


@dataclass(kw_only=True)
class ReceivedMessage(SkolaOnlineModel):
    """Received message."""

    id: str
    """ID of the message."""

    title: str | None = None
    """Subject of the message."""

    text: str | None = None
    """Message text in HTML."""

    sent_date: datetime
    """Date the message was sent."""

    read: bool
    """Whether the message was read."""

    sender: RelevantPerson | None = None
    """Sender of the message."""

    attachments_delete_date: datetime | None = None
    """Date the attachments will be deleted, set by the sender."""

    attachments_delete_text: str | None = None
    """Text shown in the message detail after the attachments are deleted from
    storage."""

    vote_options: list[str]
    """Voting options."""

    vote_answer: str | None = None
    """Answer selected by the recipient in a poll."""

    attachments: list[MessageAttachment]
    """Attachments of the message."""

    involve: str | None = None
    """Person or class the message relates to."""


@dataclass(kw_only=True)
class ReceivedMessagesResponse(SkolaOnlineModel):
    """Received messages."""

    message: str | None = None
    """Warning for the user when a non-essential part of the operation failed."""

    messages: list[ReceivedMessage]
    """Messages."""


@dataclass(kw_only=True)
class RecipientPerson(SkolaOnlineModel):
    """Person receiving a message."""

    id: str
    """ID of the recipient."""

    type: UserType | None = None
    """Type of recipient."""

    first_name: str | None = None
    """First name of the recipient."""

    last_name: str
    """Surname of the recipient."""

    title_before: str | None = None
    """Title before the name."""

    title_after: str | None = None
    """Title after the name."""

    display_name: str | None = None
    """Full name with titles."""

    persons_initials: str
    """Initials."""

    class_name: str | None = None
    """Name of the class of the student."""

    date_read: datetime | None = None
    """Date and time the message was read."""

    vote_answer: str | None = None
    """Answer selected by the recipient in a poll."""

    children: list[UserChild]
    """Children of the recipient."""


@dataclass(kw_only=True)
class RecipientsWithoutContactsData(SkolaOnlineModel):
    """Recipients without an email address or mobile phone number."""

    recipients_ids: list[str]
    """IDs of the message recipients."""

    form_of_delivery: FormOfDelivery | None = None
    """Requested form of delivery."""


@dataclass(kw_only=True)
class RelevantPerson(SkolaOnlineModel):
    """Other party of a message: the sender of a received message or the recipient of
    a sent one."""

    id: str
    """ID of the sender or recipient."""

    type: UserType | None = None
    """Type of the sender or recipient."""

    name: str
    """Name of the sender or recipient."""

    persons_initials: str
    """Initials."""

    contact_id: str | None = None
    """ID of the sender or recipient in the contact picker format."""

    detail_name: str | None = None
    """Detailed information about the person."""

    icon: AvatarIcon | None = None
    """Icon shown next to the name."""


@dataclass(kw_only=True)
class RelevantPersonChild(SkolaOnlineModel):
    """Child of a parent in the selected class."""

    id: str
    """ID of the child."""

    first_name: str | None = None
    """First name of the child."""

    last_name: str
    """Surname of the child."""

    display_name: str
    """Full name of the child."""


@dataclass(kw_only=True)
class RelevantPersonRecipient(SkolaOnlineModel):
    """Recipient of a message."""

    id: str
    """ID of the sender or recipient."""

    type: UserType | None = None
    """Type of the sender or recipient."""

    name: str
    """Name of the sender or recipient."""

    persons_initials: str
    """Initials."""

    contact_id: str | None = None
    """ID of the sender or recipient in the contact picker format."""

    detail_name: str | None = None
    """Detailed information about the person."""

    icon: AvatarIcon | None = None
    """Icon shown next to the name."""

    is_group: bool
    """Whether the recipient is a group."""

    up_group_name: str | None = None
    """Name of the parent group."""

    children_class_name: str | None = None
    """Name of the class of the child."""

    children: list[RelevantPersonChild]
    """Children of the parent in the selected class."""


@dataclass(kw_only=True)
class SendDraftMessageData(SkolaOnlineModel):
    """Draft message to send."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    title: str
    """Subject of the message."""

    text: str
    """Message text."""

    recipients: list[str]
    """IDs of the recipients."""

    previous_message_id: str | None = None
    """ID of the previous message. Only set when replying to a message."""

    attachments: list[str]
    """IDs of attached files. Upload the files before sending the message."""

    send_as_email: bool
    """Whether to send the message as an email."""

    send_as_sms: bool
    """Whether to send the message as a text message."""

    send_as_system_message: bool
    """Whether to send the message as an in-app message."""

    sender_of_email: str | None = None
    """Email address used as the sender of emails. The value self uses the address of
    the recipient."""

    attachments_delete_date: datetime | None = None
    """Date the attachments will be deleted, set by the sender."""

    vote_options: list[str]
    """Voting options."""

    attachments_delete: list[str]
    """Attachments of the draft to delete."""


@dataclass(kw_only=True)
class SentMessage(SkolaOnlineModel):
    """Sent message."""

    id: str
    """ID of the message."""

    title: str | None = None
    """Subject of the message."""

    text: str | None = None
    """Message text in HTML."""

    sent_date: datetime
    """Date the message was sent."""

    recipients: list[RelevantPersonRecipient]
    """Recipient groups of the message."""

    recipients_persons: list[RecipientPerson]
    """Recipient persons of the message."""

    number_of_recipients: int
    """Number of recipients."""

    number_of_read: int
    """Number of recipients who read the message."""

    number_of_voted: int
    """Number of recipients who voted."""

    vote_options: list[str]
    """Voting options."""

    vote_results: list[int]
    """Vote counts for the individual answers, in the order of the voting options."""

    message_forms: list[SendingType] | None = None
    """Ways the message was sent."""

    attachments_delete_date: datetime | None = None
    """Date the attachments will be deleted, set by the sender."""

    attachments_delete_text: str | None = None
    """Text shown in the message detail after the attachments are deleted from
    storage."""

    attachments: list[MessageAttachment]
    """Attachments of the message."""


@dataclass(kw_only=True)
class SentMessagesResponse(SkolaOnlineModel):
    """Sent messages."""

    message: str | None = None
    """Warning for the user when a non-essential part of the operation failed."""

    messages: list[SentMessage]
    """Messages."""


@dataclass(kw_only=True)
class UpdateMessageData(SkolaOnlineModel):
    """Updated data of a draft message."""

    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    title: str | None = None
    """Subject of the message."""

    text: str | None = None
    """Message text."""

    recipients: list[str]
    """IDs of the recipients."""

    attachments_delete_date: datetime | None = None
    """Date the attachments will be deleted, set by the sender."""

    vote_options: list[str]
    """Voting options."""

    attachments: list[str]
    """Attachments of the message."""

    attachments_delete: list[str]
    """Attachments of the draft to delete."""

    send_as_email: bool
    """Whether the message is sent as an email."""

    send_as_sms: bool
    """Whether the message is sent as a text message."""

    send_as_system_message: bool
    """Whether the message is sent as an in-app message."""

    sender_of_email: str | None = None
    """Sender of the email."""
