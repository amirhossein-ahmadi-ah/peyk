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

async def get_custom_emoji_stickers(self, custom_emoji_ids: Sequence[str]) -> List[Sticker]:
    """Use this method to get information about custom emoji stickers by their identifiers. Returns an Array of Sticker objects.

Args:
    custom_emoji_ids: A JSON-serialized list of custom emoji identifiers. At most 200 custom emoji identifiers can be specified.

Returns:
    List[Sticker]: Result returned by Telegram on successful execution."""
    result = await self._call('getCustomEmojiStickers', json_body={'custom_emoji_ids': list(custom_emoji_ids)})
    return Sticker.list_from(result) or []
