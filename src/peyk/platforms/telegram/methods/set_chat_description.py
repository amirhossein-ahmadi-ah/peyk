from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def set_chat_description(self, chat_id: ChatId, description: Optional[str]=None) -> bool:
    """Use this method to change the description of a group, a supergroup or a channel. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    description: New chat description, 0-255 characters

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id}
    if description is not None:
        payload['description'] = description
    return bool(await self._call('setChatDescription', json_body=payload))
