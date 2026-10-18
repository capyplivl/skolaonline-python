from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import ClassVar

from skolaonline.models._base import SkolaOnlineModel
from skolaonline.models.common import UserType
from skolaonline.models.user import UserChild


class AvatarIcon(StrEnum):
    STUDENT = "student"
    STUDENT_AND_PARENT = "studentAndParent"
    PARENT = "parent"
    PRIMARY_PARENT = "primaryParent"
    EMPLOYEE = "employee"


class ConceptMessageOrder(StrEnum):
    DATE_SAVE_DESC = "dateSaveDesc"
    DATE_SAVE_ASC = "dateSaveAsc"


class FormOfDelivery(StrEnum):
    MAILSMS = "mailsms"
    MAIL = "mail"
    SMS = "sms"


class MessageOrder(StrEnum):
    DATE_SEND_DESC = "dateSendDesc"
    DATE_SEND_ASC = "dateSendAsc"


class MessageReadStatus(StrEnum):
    NOT_RESTRICTED = "notRestricted"
    READ = "read"
    NOT_READ = "notRead"


class SenderPersonType(StrEnum):
    NOT_RESTRICTED = "notRestricted"
    STUDENT = "student"
    PARENT = "parent"
    EMPLOYEE = "employee"


class SendingType(StrEnum):
    SMS = "sms"
    EMAIL = "email"
    SYSTEM_MESSAGE = "systemMessage"
    SYSTEM_MESSAGE_WITH_VOTE = "systemMessageWithVote"


@dataclass(kw_only=True)
class ConceptMessage(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    id: str
    title: str | None = None
    text: str | None = None
    save_date: datetime
    recipients: list[RelevantPerson]
    attachments_delete_date: datetime | None = None
    attachments_delete_text: str | None = None
    vote_options: list[str]
    attachments: list[MessageAttachment]
    send_as_email: bool
    send_as_sms: bool
    send_as_system_message: bool
    sender_of_email: str | None = None
    previous_message_id: str | None = None


@dataclass(kw_only=True)
class ConceptMessagesResponse(SkolaOnlineModel):
    message: str | None = None
    messages: list[ConceptMessage]


@dataclass(kw_only=True)
class DraftMessageData(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    previous_message_id: str | None = None
    attachments: list[str]
    send_as_email: bool
    send_as_sms: bool
    send_as_system_message: bool
    sender_of_email: str | None = None
    attachments_delete_date: datetime | None = None
    vote_options: list[str]
    title: str | None = None
    text: str | None = None
    recipients: list[str]


@dataclass(kw_only=True)
class GetMessageRecipientsCountRequest(SkolaOnlineModel):
    recipients_groups: list[str]


@dataclass(kw_only=True)
class MessageAttachment(SkolaOnlineModel):
    id: str
    name: str
    name_user: str | None = None
    type: str | None = None
    size: int


@dataclass(kw_only=True)
class MessageData(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    title: str
    text: str
    recipients: list[str]
    previous_message_id: str | None = None
    attachments: list[str]
    send_as_email: bool
    send_as_sms: bool
    send_as_system_message: bool
    sender_of_email: str | None = None
    attachments_delete_date: datetime | None = None
    vote_options: list[str]


@dataclass(kw_only=True)
class MessagesFormsResponse(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "implicit_sms": "implicitSMS",
    }

    system_message: bool
    email: bool
    sender_of_email: list[str]
    sms: bool
    attachment: bool
    implicit_system_message: bool
    implicit_email: bool
    implicit_sms: bool
    alert_number_of_recipients: int | None = None
    list_of_voting_options: list[list[str]]
    max_attachment_size: int | None = None


@dataclass(kw_only=True)
class PostMessageVoteRequest(SkolaOnlineModel):
    vote_answer: str | None = None


@dataclass(kw_only=True)
class ReceivedMessage(SkolaOnlineModel):
    id: str
    title: str | None = None
    text: str | None = None
    sent_date: datetime
    read: bool
    sender: RelevantPerson | None = None
    attachments_delete_date: datetime | None = None
    attachments_delete_text: str | None = None
    vote_options: list[str]
    vote_answer: str | None = None
    attachments: list[MessageAttachment]
    involve: str | None = None


@dataclass(kw_only=True)
class ReceivedMessagesResponse(SkolaOnlineModel):
    message: str | None = None
    messages: list[ReceivedMessage]


@dataclass(kw_only=True)
class RecipientPerson(SkolaOnlineModel):
    id: str
    type: UserType | None = None
    first_name: str | None = None
    last_name: str
    title_before: str | None = None
    title_after: str | None = None
    display_name: str | None = None
    persons_initials: str
    class_name: str | None = None
    date_read: datetime | None = None
    vote_answer: str | None = None
    children: list[UserChild]


@dataclass(kw_only=True)
class RecipientsWithoutContactsData(SkolaOnlineModel):
    recipients_ids: list[str]
    form_of_delivery: FormOfDelivery | None = None


@dataclass(kw_only=True)
class RelevantPerson(SkolaOnlineModel):
    id: str
    type: UserType | None = None
    name: str
    persons_initials: str
    contact_id: str | None = None
    detail_name: str | None = None
    icon: AvatarIcon | None = None


@dataclass(kw_only=True)
class RelevantPersonChild(SkolaOnlineModel):
    id: str
    first_name: str | None = None
    last_name: str
    display_name: str


@dataclass(kw_only=True)
class RelevantPersonRecipient(SkolaOnlineModel):
    id: str
    type: UserType | None = None
    name: str
    persons_initials: str
    contact_id: str | None = None
    detail_name: str | None = None
    icon: AvatarIcon | None = None
    is_group: bool
    up_group_name: str | None = None
    children_class_name: str | None = None
    children: list[RelevantPersonChild]


@dataclass(kw_only=True)
class SendDraftMessageData(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    title: str
    text: str
    recipients: list[str]
    previous_message_id: str | None = None
    attachments: list[str]
    send_as_email: bool
    send_as_sms: bool
    send_as_system_message: bool
    sender_of_email: str | None = None
    attachments_delete_date: datetime | None = None
    vote_options: list[str]
    attachments_delete: list[str]


@dataclass(kw_only=True)
class SentMessage(SkolaOnlineModel):
    id: str
    title: str | None = None
    text: str | None = None
    sent_date: datetime
    recipients: list[RelevantPersonRecipient]
    recipients_persons: list[RecipientPerson]
    number_of_recipients: int
    number_of_read: int
    number_of_voted: int
    vote_options: list[str]
    vote_results: list[int]
    message_forms: list[SendingType] | None = None
    attachments_delete_date: datetime | None = None
    attachments_delete_text: str | None = None
    attachments: list[MessageAttachment]


@dataclass(kw_only=True)
class SentMessagesResponse(SkolaOnlineModel):
    message: str | None = None
    messages: list[SentMessage]


@dataclass(kw_only=True)
class UpdateMessageData(SkolaOnlineModel):
    _field_aliases: ClassVar[dict[str, str]] = {
        "send_as_sms": "sendAsSMS",
    }

    title: str | None = None
    text: str | None = None
    recipients: list[str]
    attachments_delete_date: datetime | None = None
    vote_options: list[str]
    attachments: list[str]
    attachments_delete: list[str]
    send_as_email: bool
    send_as_sms: bool
    send_as_system_message: bool
    sender_of_email: str | None = None
