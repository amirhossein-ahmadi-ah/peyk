"""Normalized membership-transition contracts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional, Union

Identifier = Union[int, str]


@dataclass(frozen=True)
class IncomingChatMemberStatusUpdate:
    """Rich Telegram-style member status transition.

    ``actor_id`` is optional by design; an adapter must never invent it.
    """

    chat_id: Optional[Identifier] = None
    actor_id: Optional[Identifier] = None
    target_user_id: Optional[Identifier] = None
    old_status: Optional[str] = None
    new_status: Optional[str] = None
    old_is_member: Optional[bool] = None
    new_is_member: Optional[bool] = None
    date: Optional[int] = None
    raw: object = None


@dataclass(frozen=True)
class IncomingBotMembershipChange:
    """Simple bot-added/bot-removed event.

    Rubika provides this explicitly through EventData; Telegram/Bale can
    derive it from new/left chat-member message fields when the bot itself is
    the member mentioned there.  ``actor_id`` remains optional.
    """

    chat_id: Optional[Identifier] = None
    added: bool = False
    actor_id: Optional[Identifier] = None
    raw: object = None
