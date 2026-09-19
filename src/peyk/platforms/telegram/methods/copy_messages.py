from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def copy_messages(self, chat_id: ChatId, from_chat_id: ChatId, message_ids: Sequence[int], *, message_thread_id: Optional[int]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, remove_caption: Optional[bool]=None) -> List[MessageId]:
    """Use this method to copy messages of any kind. If some of the specified messages can't be found or copied, they are skipped. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_id is known to the bot. The method is analogous to the method forwardMessages, but the copied messages don't have a link to the original message. Album grouping is kept for copied messages. On success, an Array of MessageId of the sent messages is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    from_chat_id: Unique identifier for the chat where the original messages were sent (or username of the target bot, supergroup or channel in the format @username)
    message_ids: A JSON-serialized list of 1-100 identifiers of messages in the chat from_chat_id to copy. The identifiers must be specified in a strictly increasing order.
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    disable_notification: Sends the messages silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent messages from forwarding and saving
    remove_caption: Pass True to copy the messages without their captions

Returns:
    List[MessageId]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_ids': list(message_ids)}
    if message_thread_id is not None:
        payload['message_thread_id'] = message_thread_id
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if protect_content is not None:
        payload['protect_content'] = protect_content
    if remove_caption is not None:
        payload['remove_caption'] = remove_caption
    result = await self._call('copyMessages', json_body=payload)
    return [MessageId.from_dict(item) for item in result or []]
