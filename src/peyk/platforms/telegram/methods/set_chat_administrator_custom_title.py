from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def set_chat_administrator_custom_title(self, chat_id: ChatId, user_id: int, custom_title: str) -> bool:
    """Use this method to set a custom title for an administrator in a supergroup promoted by the bot. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    user_id: Unique identifier of the target user
    custom_title: New custom title for the administrator; 0-16 characters, emoji are not allowed

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload = {'chat_id': chat_id, 'user_id': user_id, 'custom_title': custom_title}
    return bool(await self._call('setChatAdministratorCustomTitle', json_body=payload))
