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

async def set_sticker_set_thumbnail(self, name: str, user_id: int, *, thumbnail: Optional[MediaInput]=None, format: Optional[str]=None) -> bool:
    """Use this method to set the thumbnail of a regular or mask sticker set. The format of the thumbnail file must match the format of the stickers in the set. Returns True on success.

Args:
    name: Sticker set name
    user_id: User identifier of the sticker set owner
    thumbnail: A .WEBP or .PNG image with the thumbnail, must be up to 128 kilobytes in size and have a width and height of exactly 100px, or a .TGS animation with a thumbnail up to 32 kilobytes in size (see https://core.telegram.org/stickers#animation-requirements for animated sticker technical requirements), or a .WEBM video with the thumbnail up to 32 kilobytes in size; see https://core.telegram.org/stickers#video-requirements for video sticker technical requirements. Pass a file_id as a String to send a file that already exists on the Telegram servers, pass an HTTP URL as a String for Telegram to get a file from the Internet, or upload a new one using multipart/form-data. More information on Sending Files. Animated and video sticker set thumbnails can't be uploaded via HTTP URL. If omitted, then the thumbnail is dropped and the first sticker is used as the thumbnail.
    format: Format of the thumbnail, must be one of 'static' for a .WEBP or .PNG image, 'animated' for a .TGS animation, or 'video' for a .WEBM video

Returns:
    bool: Result returned by Telegram on successful execution."""
    if thumbnail is None and format is None:
        return bool(await self._call('setStickerSetThumbnail', json_body={'name': name, 'user_id': user_id}))
    if not self._is_upload(thumbnail):
        payload: Dict[str, object] = {'name': name, 'user_id': user_id, 'thumbnail': thumbnail}
        if format is not None:
            payload['format'] = format
        return bool(await self._call('setStickerSetThumbnail', json_body=payload))
    fields: Dict[str, str] = {'name': name, 'user_id': str(user_id)}
    if format is not None:
        fields['format'] = format
    files: Dict[str, FilePayload] = {'thumbnail': self._as_file_payload(thumbnail, default_filename='thumbnail.png')}
    return bool(await self._call('setStickerSetThumbnail', data=fields, files=files))
