"""Platform-neutral incoming message contracts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Union

Identifier = Union[int, str]


@dataclass(frozen=True)
class IncomingMessage:
    """Normalized message surface shared by the three platform adapters.

    IDs deliberately retain their source scalar type because Telegram/Bale use
    integers while Rubika uses string IDs.  Missing source data remains None.
    ``raw`` always points at the exact source model instance.
    """

    message_id: Optional[Identifier] = None
    chat_id: Optional[Identifier] = None
    chat_type: Optional[str] = None
    sender_id: Optional[Identifier] = None
    text: Optional[str] = None
    date: Optional[int] = None
    is_edited: bool = False
    update_kind: str = "message"
    reply_to_message_id: Optional[Identifier] = None
    media: object = None
    new_chat_members: Optional[list[Identifier]] = None
    left_chat_member: Optional[Identifier] = None
    successful_payment: object = None
    raw: object = None


@dataclass(frozen=True)
class IncomingMessageDeleted:
    """A deletion event where the platform exposes no replacement message."""

    chat_id: Optional[Identifier] = None
    message_id: Optional[Identifier] = None
    raw: object = None
