from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .user import User

@dataclass
class ChatInviteLink:
    """Represents an invite link for a chat.

Attributes:
    invite_link: The invite link. If the link was created by another chat administrator, then the second part of the link will be replaced with '…'.
    creator: Creator of the link
    creates_join_request: True, if users joining the chat via the link need to be approved by chat administrators
    is_primary: True, if the link is primary
    is_revoked: True, if the link is revoked
    name: Invite link name
    expire_date: Point in time (Unix timestamp) when the link will expire or has been expired
    member_limit: The maximum number of users that can be members of the chat simultaneously after joining the chat via this invite link; 1-99999
    pending_join_request_count: Number of pending join requests created using this link
    subscription_period: The number of seconds the subscription will be active for before the next payment
    subscription_price: The amount of Telegram Stars a user must pay initially and after each subsequent subscription period to be a member of the chat using the link"""
    invite_link: str
    creator: Optional[User] = None
    creates_join_request: Optional[bool] = None
    is_primary: Optional[bool] = None
    is_revoked: Optional[bool] = None
    name: Optional[str] = None
    expire_date: Optional[int] = None
    member_limit: Optional[int] = None
    pending_join_request_count: Optional[int] = None
    subscription_period: Optional[int] = None
    subscription_price: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatInviteLink']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(invite_link=data.get('invite_link', ''), creator=User.from_dict(data.get('creator')), creates_join_request=data.get('creates_join_request'), is_primary=data.get('is_primary'), is_revoked=data.get('is_revoked'), name=data.get('name'), expire_date=data.get('expire_date'), member_limit=data.get('member_limit'), pending_join_request_count=data.get('pending_join_request_count'), subscription_period=data.get('subscription_period'), subscription_price=data.get('subscription_price'))
