from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
import orjson
from peyk.transport import FilePayload
from ..errors import TelegramAPIError, ResponseParameters
from ..models import *
from .. import models as _models
globals().update({k: v for k, v in vars(_models).items() if k.startswith('_')})
from peyk.platforms.telegram.methods._resolve_sticker_ref import _resolve_sticker_ref
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def replace_sticker_in_set(self, user_id: int, name: str, old_sticker: str, sticker: InputSticker) -> bool:
    """Use this method to replace an existing sticker in a sticker set with a new one. The method is equivalent to calling deleteStickerFromSet, then addStickerToSet, then setStickerPositionInSet. Returns True on success.

Args:
    user_id: User identifier of the sticker set owner
    name: Sticker set name
    old_sticker: File identifier of the replaced sticker
    sticker: A JSON-serialized object with information about the added sticker. If exactly the same sticker had already been added to the set, then the set remains unchanged.

Returns:
    bool: Result returned by Telegram on successful execution."""
    files: Dict[str, FilePayload] = {}
    sticker_payload = sticker.to_dict(_resolve_sticker_ref(sticker.sticker, 0, files))
    if files:
        fields: Dict[str, str] = {'user_id': str(user_id), 'name': name, 'old_sticker': old_sticker, 'sticker': self._json_field(sticker_payload)}
        return bool(await self._call('replaceStickerInSet', data=fields, files=files))
    payload: Dict[str, object] = {'user_id': user_id, 'name': name, 'old_sticker': old_sticker, 'sticker': sticker_payload}
    return bool(await self._call('replaceStickerInSet', json_body=payload))
