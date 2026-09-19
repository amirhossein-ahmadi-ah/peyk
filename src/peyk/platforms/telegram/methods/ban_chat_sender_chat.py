from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def ban_chat_sender_chat(self, chat_id: ChatId, sender_chat_id: int) -> bool:
    """Use this method to ban a channel chat in a supergroup or a channel. Until the chat is unbanned, the owner of the banned chat won't be able to send messages on behalf of any of their channels. The bot must be an administrator in the supergroup or channel for this to work and must have the appropriate administrator rights. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    sender_chat_id: Unique identifier of the target sender chat

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload = {'chat_id': chat_id, 'sender_chat_id': sender_chat_id}
    return bool(await self._call('banChatSenderChat', json_body=payload))
