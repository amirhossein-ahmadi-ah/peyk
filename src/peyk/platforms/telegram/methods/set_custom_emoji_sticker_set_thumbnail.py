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

async def set_custom_emoji_sticker_set_thumbnail(self, name: str, custom_emoji_id: Optional[str]=None) -> bool:
    """Use this method to set the thumbnail of a custom emoji sticker set. Returns True on success.

Args:
    name: Sticker set name
    custom_emoji_id: Custom emoji identifier of a sticker from the sticker set; pass an empty string to drop the thumbnail and use the first sticker as the thumbnail

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'name': name}
    if custom_emoji_id is not None:
        payload['custom_emoji_id'] = custom_emoji_id
    return bool(await self._call('setCustomEmojiStickerSetThumbnail', json_body=payload))
