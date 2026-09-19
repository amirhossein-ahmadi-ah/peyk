"""Telegram chat-member status values."""

from enum import StrEnum


class ChatMemberStatus(StrEnum):
    """Finite status values used by Telegram's ChatMember union."""

    CREATOR = "creator"
    ADMINISTRATOR = "administrator"
    MEMBER = "member"
    RESTRICTED = "restricted"
    LEFT = "left"
    KICKED = "kicked"
