from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def forward_message(self, chat_id: ChatId, from_chat_id: ChatId, message_id: int, *, message_thread_id: Optional[int]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None) -> Message:
    """Use this method to forward messages of any kind. Service messages and messages with protected content can't be forwarded. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    from_chat_id: Unique identifier for the chat where the original message was sent (or username of the target bot, supergroup or channel in the format @username)
    message_id: Message identifier in the chat specified in from_chat_id
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the forwarded message from forwarding and saving

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    if message_thread_id is not None:
        payload['message_thread_id'] = message_thread_id
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if protect_content is not None:
        payload['protect_content'] = protect_content
    result = await self._call('forwardMessage', json_body=payload)
    return Message.from_dict(result)
