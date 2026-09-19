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

async def upload_sticker_file(self, user_id: int, sticker: MediaInput, sticker_format: str) -> File:
    """Use this method to upload a file with a sticker for later use in the createNewStickerSet, addStickerToSet, or replaceStickerInSet methods (the file can be used multiple times). Returns the uploaded File on success.

Args:
    user_id: User identifier of sticker file owner
    sticker: A file with the sticker in .WEBP, .PNG, .TGS, or .WEBM format. See https://core.telegram.org/stickers for technical requirements. More information on Sending Files
    sticker_format: Format of the sticker, must be one of 'static', 'animated', 'video'

Returns:
    File: Result returned by Telegram on successful execution."""
    if not self._is_upload(sticker):
        result = await self._call('uploadStickerFile', json_body={'user_id': user_id, 'sticker': sticker, 'sticker_format': sticker_format})
        return File.from_dict(result)
    fields: Dict[str, str] = {'user_id': str(user_id), 'sticker_format': sticker_format}
    files: Dict[str, FilePayload] = {'sticker': self._as_file_payload(sticker, default_filename='sticker.webp')}
    result = await self._call('uploadStickerFile', data=fields, files=files)
    return File.from_dict(result)
