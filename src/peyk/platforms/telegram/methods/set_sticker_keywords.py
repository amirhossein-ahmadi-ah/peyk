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

async def set_sticker_keywords(self, sticker: str, keywords: Optional[List[str]]=None) -> bool:
    """Use this method to change search keywords assigned to a regular or custom emoji sticker. The sticker must belong to a sticker set created by the bot. Returns True on success.

Args:
    sticker: File identifier of the sticker
    keywords: A JSON-serialized list of 0-20 search keywords for the sticker with total length of up to 64 characters

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'sticker': sticker}
    if keywords is not None:
        payload['keywords'] = list(keywords)
    return bool(await self._call('setStickerKeywords', json_body=payload))
