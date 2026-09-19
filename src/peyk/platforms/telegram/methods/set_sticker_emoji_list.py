from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
import orjson
from peyk.transport import FilePayload
from ..errors import TelegramAPIError, ResponseParameters
from ..models import *
from .. import models as _models
globals().update({k: v for k, v in vars(_models).items() if k.startswith('_')})
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def set_sticker_emoji_list(self, sticker: str, emoji_list: List[str]) -> bool:
    """Use this method to change the list of emoji assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success.

Args:
    sticker: File identifier of the sticker
    emoji_list: A JSON-serialized list of 1-20 emoji associated with the sticker

Returns:
    bool: Result returned by Telegram on successful execution."""
    return bool(await self._call('setStickerEmojiList', json_body={'sticker': sticker, 'emoji_list': list(emoji_list)}))
