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

async def set_sticker_set_title(self, name: str, title: str) -> bool:
    """Use this method to set the title of a created sticker set. Returns True on success.

Args:
    name: Sticker set name
    title: Sticker set title, 1-64 characters

Returns:
    bool: Result returned by Telegram on successful execution."""
    return bool(await self._call('setStickerSetTitle', json_body={'name': name, 'title': title}))
