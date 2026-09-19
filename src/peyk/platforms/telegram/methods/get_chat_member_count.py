from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def get_chat_member_count(self, chat_id: ChatId) -> int:
    """Use this method to get the number of members in a chat. Returns Integer on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup or channel in the format @username

Returns:
    int: Result returned by Telegram on successful execution."""
    return await self._get_chat_member_count(chat_id)
