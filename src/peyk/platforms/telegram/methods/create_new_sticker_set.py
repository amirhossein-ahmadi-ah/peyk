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

async def create_new_sticker_set(self, user_id: int, name: str, title: str, stickers: Sequence[InputSticker], *, sticker_type: Optional[str]=None, needs_repainting: Optional[bool]=None) -> bool:
    """Use this method to create a new sticker set owned by a user. The bot will be able to edit the sticker set thus created. Returns True on success.

Args:
    user_id: User identifier of created sticker set owner
    name: Short name of sticker set, to be used in t.me/addstickers/ URLs (e.g., animals). Can contain only English letters, digits and underscores. Must begin with a letter, can't contain consecutive underscores and must end in "_by_".  is case insensitive. 1-64 characters.
    title: Sticker set title, 1-64 characters
    stickers: A JSON-serialized list of 1-50 initial stickers to be added to the sticker set
    sticker_type: Type of stickers in the set, pass 'regular', 'mask', or 'custom_emoji'. By default, a regular sticker set is created.
    needs_repainting: Pass True if stickers in the sticker set must be repainted to the color of text when used in messages, the accent color if used as emoji status, white on chat photos, or another appropriate color based on context; for custom emoji sticker sets only

Returns:
    bool: Result returned by Telegram on successful execution."""
    files: Dict[str, FilePayload] = {}
    stickers_payload = [s.to_dict(_resolve_sticker_ref(s.sticker, i, files)) for i, s in enumerate(stickers)]
    if files:
        fields: Dict[str, str] = {'user_id': str(user_id), 'name': name, 'title': title, 'stickers': self._json_field(stickers_payload)}
        if sticker_type is not None:
            fields['sticker_type'] = sticker_type
        if needs_repainting is not None:
            fields['needs_repainting'] = str(needs_repainting)
        return bool(await self._call('createNewStickerSet', data=fields, files=files))
    payload: Dict[str, object] = {'user_id': user_id, 'name': name, 'title': title, 'stickers': stickers_payload}
    if sticker_type is not None:
        payload['sticker_type'] = sticker_type
    if needs_repainting is not None:
        payload['needs_repainting'] = needs_repainting
    return bool(await self._call('createNewStickerSet', json_body=payload))
