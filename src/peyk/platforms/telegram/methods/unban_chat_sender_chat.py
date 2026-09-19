from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def unban_chat_sender_chat(self, chat_id: ChatId, sender_chat_id: int) -> bool:
    """Use this method to unban a previously banned channel chat in a supergroup or channel. The bot must be an administrator for this to work and must have the appropriate administrator rights. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    sender_chat_id: Unique identifier of the target sender chat

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload = {'chat_id': chat_id, 'sender_chat_id': sender_chat_id}
    return bool(await self._call('unbanChatSenderChat', json_body=payload))
