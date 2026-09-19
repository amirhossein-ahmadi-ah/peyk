from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def send_media_group(self, chat_id: ChatId, media: Sequence[InputMediaItem], *, message_thread_id: Optional[int]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None) -> List[Message]:
    """Use this method to send a group of photos, live photos, videos, documents or audios as an album. Documents and audio files can be only grouped in an album with messages of the same type. On success, an Array of Message objects that were sent is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    media: A JSON-serialized Array describing messages to be sent, must include 2-10 items
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    disable_notification: Sends messages silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent messages from forwarding and saving
    reply_parameters: Description of the message to reply to

Returns:
    List[Message]: Result returned by Telegram on successful execution."""
    files: Dict[str, FilePayload] = {}
    media_payload = [self._resolve_album_item(item, index, files) for index, item in enumerate(media)]
    if files:
        fields: Dict[str, str] = {'chat_id': str(chat_id), 'media': self._json_field(media_payload)}
        self._apply_send_options_form(fields, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters)
        result = await self._call('sendMediaGroup', data=fields, files=files)
    else:
        payload: Dict[str, object] = {'chat_id': chat_id, 'media': media_payload}
        self._apply_send_options_json(payload, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters)
        result = await self._call('sendMediaGroup', json_body=payload)
    return Message.list_from_result(result)
