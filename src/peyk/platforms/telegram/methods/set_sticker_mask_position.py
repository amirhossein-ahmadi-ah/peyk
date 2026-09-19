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

async def set_sticker_mask_position(self, sticker: str, mask_position: Optional[MaskPosition]=None) -> bool:
    """Use this method to change the mask position of a mask sticker. The sticker must belong to a sticker set that was created by the bot. Returns True on success.

Args:
    sticker: File identifier of the sticker
    mask_position: A JSON-serialized object with the position where the mask should be placed on faces. Omit the parameter to remove the mask position.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'sticker': sticker}
    if mask_position is not None:
        payload['mask_position'] = mask_position.to_dict()
    return bool(await self._call('setStickerMaskPosition', json_body=payload))
