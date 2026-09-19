from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def set_chat_photo(self, chat_id: ChatId, photo: MediaInput) -> bool:
    """Use this method to set a new profile photo for the chat. Photos can't be changed for private chats. The bot must be an administrator in the chat for this to work and must have the appropriate administrator rights. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel in the format @username
    photo: New chat photo, uploaded using multipart/form-data

Returns:
    bool: Result returned by Telegram on successful execution."""
    if isinstance(photo, str):
        raise ValueError('set_chat_photo: photo must be upload content (bytes/stream/FilePayload), not a file_id/URL string')
    fields: Dict[str, str] = {'chat_id': str(chat_id)}
    files = {'photo': self._as_file_payload(photo, default_filename='chat_photo.jpg')}
    return bool(await self._call('setChatPhoto', data=fields, files=files))
