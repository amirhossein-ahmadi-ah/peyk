from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def delete_chat_sticker_set(self, chat_id: ChatId) -> bool:
    """Use this method to delete a group sticker set from a supergroup. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Use the field can_set_sticker_set optionally returned in getChat requests to check if the bot can use this method. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username

Returns:
    bool: Result returned by Telegram on successful execution."""
    return bool(await self._call('deleteChatStickerSet', json_body={'chat_id': chat_id}))
