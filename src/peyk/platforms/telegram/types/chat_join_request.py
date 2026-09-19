from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from peyk.bot.base import Bot
from .chat import Chat
from .chat_invite_link import ChatInviteLink
from .user import User

@dataclass
class ChatJoinRequest:
    """Represents a join request sent to a chat.

Attributes:
    chat: Chat to which the request was sent
    from: User that sent the join request
    user_chat_id: Identifier of a private chat with the user who sent the join request. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier. The bot can use this identifier for 5 minutes to send messages until the join request is processed, assuming no other administrator contacted the user.
    date: Date the request was sent in Unix time
    bio: Bio of the user
    invite_link: Chat invite link that was used by the user to send the join request
    query_id: Identifier of the join request query; for bots assigned to process join requests only. If present, then the bot must call sendChatJoinRequestWebApp or directly call answerChatJoinRequestQuery within 10 seconds."""
    chat: Chat
    from_: Optional[User] = None
    user_chat_id: Optional[int] = None
    date: Optional[int] = None
    bio: Optional[str] = None
    invite_link: Optional[ChatInviteLink] = None
    query_id: Optional[str] = None
    bot: Optional['Bot[object]'] = field(default=None, repr=False, compare=False)

    async def approve(self) -> bool:
        """Approve this join request through the injected bot."""
        if self.bot is None or self.from_ is None:
            raise RuntimeError('ChatJoinRequest is not bound to a Bot')
        return await self.bot.client.approve_chat_join_request(self.chat.id, self.from_.id)

    async def decline(self) -> bool:
        """Decline this join request through the injected bot."""
        if self.bot is None or self.from_ is None:
            raise RuntimeError('ChatJoinRequest is not bound to a Bot')
        return await self.bot.client.decline_chat_join_request(self.chat.id, self.from_.id)

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ChatJoinRequest']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(chat=Chat.from_dict(data.get('chat', {})), from_=User.from_dict(data.get('from')), user_chat_id=data.get('user_chat_id'), date=data.get('date'), bio=data.get('bio'), invite_link=ChatInviteLink.from_dict(data.get('invite_link')), query_id=data.get('query_id'))
