from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def set_chat_sticker_set(self, chat_id: ChatId, sticker_set_name: str) -> bool:
    """Use this method to set a new group sticker set for a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    sticker_set_name: Name of the sticker set to be set as the group sticker set

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload = {'chat_id': chat_id, 'sticker_set_name': sticker_set_name}
    return bool(await self._call('setChatStickerSet', json_body=payload))
