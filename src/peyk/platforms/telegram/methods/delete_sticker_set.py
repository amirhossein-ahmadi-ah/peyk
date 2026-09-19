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

async def delete_sticker_set(self, name: str) -> bool:
    """Use this method to delete a sticker set that was created by the bot. Returns True on success.

Args:
    name: Sticker set name

Returns:
    bool: Result returned by Telegram on successful execution."""
    return bool(await self._call('deleteStickerSet', json_body={'name': name}))
