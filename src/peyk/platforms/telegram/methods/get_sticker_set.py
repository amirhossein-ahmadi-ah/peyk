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

async def get_sticker_set(self, name: str) -> StickerSet:
    """Use this method to get a sticker set. On success, a StickerSet object is returned.

Args:
    name: Name of the sticker set

Returns:
    StickerSet: Result returned by Telegram on successful execution."""
    result = await self._call('getStickerSet', json_body={'name': name})
    return StickerSet.from_dict(result)
