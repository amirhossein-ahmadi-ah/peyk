from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def edit_message_media(self, media: InputMediaItem, *, chat_id: Optional[ChatId]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, reply_markup: Optional[ReplyMarkup]=None) -> Union[Message, bool]:
    """Use this method to edit animation, audio, document, live photo, photo, or video messages, or to replace a text or a rich message with a media. If a message is part of a message album, then it can be edited only to an audio for audio albums, only to a document for document albums and to a photo, a live photo, or a video otherwise. When an inline message is edited, a new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.

Args:
    media: A JSON-serialized object for the new media content of the message
    chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
    message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    reply_markup: A JSON-serialized object for a new inline keyboard

Returns:
    Union[Message, bool]: Result returned by Telegram on successful execution."""
    target = self._edit_target(chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, method='edit_message_media')
    if inline_message_id is not None:
        files: Dict[str, FilePayload] = {}
        entry = self._resolve_album_item(media, 0, files)
        if files:
            raise ValueError('edit_message_media: inline messages cannot upload new files; use a file_id or URL')
        payload: Dict[str, object] = {**target, 'media': entry}
        if reply_markup is not None:
            payload['reply_markup'] = serialize_reply_markup(reply_markup)
        result = await self._call('editMessageMedia', json_body=payload)
        if isinstance(result, bool):
            return result
        return Message.from_dict(result)
    files = {}
    entry = self._resolve_album_item(media, 0, files)
    if files:
        fields: Dict[str, str] = {key: str(value) for key, value in target.items()}
        fields['media'] = self._json_field(entry)
        if reply_markup is not None:
            fields['reply_markup'] = self._json_field(serialize_reply_markup(reply_markup))
        result = await self._call('editMessageMedia', data=fields, files=files)
    else:
        payload = {**target, 'media': entry}
        if reply_markup is not None:
            payload['reply_markup'] = serialize_reply_markup(reply_markup)
        result = await self._call('editMessageMedia', json_body=payload)
    if isinstance(result, bool):
        return result
    return Message.from_dict(result)
