from __future__ import annotations
from ..errors import BaleAPIError
from peyk.transport import FilePayload
from ..models import Message
from typing import Any, Dict, List, Optional, Sequence, Union
from ..types.input_media_item import InputMediaItem, _INPUT_MEDIA_TYPE_NAMES
from ..types.input_media_animation import InputMediaAnimation
from ..types.input_media_audio import InputMediaAudio
from ..types.input_media_video import InputMediaVideo

async def send_media_group(self, chat_id: Union[int, str], media: Sequence[InputMediaItem], *, reply_to_message_id: Optional[int]=None) -> List[Message]:
    """Sends media group through the Bale API.

Args:
    chat_id: Identifier of the target chat.
    media: Value used by this operation.
    reply_to_message_id: Value used by this operation.

Returns:
    Result produced by the Bale operation."""
    'Send an album of photos/videos/documents/audio in one message group.\n    \n            `media` items with a `str` `media` value (file_id or URL) are\n            sent as plain JSON; items carrying raw upload content (bytes, a\n            stream, or a `FilePayload`) are switched to `attach://<name>`\n            references with a matching multipart file part, exactly like a\n            single upload just with a generated per-item attachment name. If\n            *any* item needs an upload, the whole request goes out as\n            multipart (Bale, like the Telegram-shaped APIs it mirrors here,\n            allows JSON-array fields alongside file parts in the same\n            multipart body).\n            \n    \n    Args:\n        chat_id: Value of the declared parameter type.\n        media: Value of the declared parameter type.\n        reply_to_message_id: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``List[Message]``).\n    '
    media_payload: List[Dict[str, object]] = []
    files: Dict[str, FilePayload] = {}
    for index, item in enumerate(media):
        type_name = _INPUT_MEDIA_TYPE_NAMES[type(item)]
        entry: Dict[str, object] = {'type': type_name}
        if self._is_upload(item.media):
            attach_name = f'file{index}'
            entry['media'] = f'attach://{attach_name}'
            files[attach_name] = self._as_file_payload(item.media, default_filename=f'{type_name}_{index}')
        else:
            entry['media'] = item.media
        if item.caption is not None:
            entry['caption'] = item.caption
        if isinstance(item, (InputMediaVideo, InputMediaAnimation)):
            if item.width is not None:
                entry['width'] = item.width
            if item.height is not None:
                entry['height'] = item.height
            if item.duration is not None:
                entry['duration'] = item.duration
        if isinstance(item, InputMediaAudio):
            if item.duration is not None:
                entry['duration'] = item.duration
            if item.title is not None:
                entry['title'] = item.title
        media_payload.append(entry)
    if files:
        fields: Dict[str, str] = {'chat_id': str(chat_id), 'media': self._json_field(media_payload)}
        if reply_to_message_id is not None:
            fields['reply_to_message_id'] = str(reply_to_message_id)
        result = await self._call('sendMediaGroup', data=fields, files=files)
    else:
        payload: Dict[str, object] = {'chat_id': chat_id, 'media': media_payload}
        if reply_to_message_id is not None:
            payload['reply_to_message_id'] = reply_to_message_id
        result = await self._call('sendMediaGroup', json_body=payload)
    return Message.list_from_result(result)
