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

async def set_sticker_position_in_set(self, sticker: str, position: int) -> bool:
    """Use this method to move a sticker in a set created by the bot to a specific position. Returns True on success.

Args:
    sticker: File identifier of the sticker
    position: New sticker position in the set, zero-based

Returns:
    bool: Result returned by Telegram on successful execution."""
    return bool(await self._call('setStickerPositionInSet', json_body={'sticker': sticker, 'position': position}))
