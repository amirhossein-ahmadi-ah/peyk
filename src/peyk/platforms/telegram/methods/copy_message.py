from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]
from ._serialization import _serialize_entities, _serialize_reply_parameters, _serialize_link_preview

async def copy_message(self, chat_id: ChatId, from_chat_id: ChatId, message_id: int, *, message_thread_id: Optional[int]=None, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[EntitiesInput]=None, show_caption_above_media: Optional[bool]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> message:
    """Use this method to copy messages of any kind. Service messages, paid media messages, giveaway messages, giveaway winners messages, and invoice messages can't be copied. A quiz poll can be copied only if the value of the field correct_option_id is known to the bot. The method is analogous to the method forwardMessage, but the copied message doesn't have a link to the original message. Returns the MessageId of the sent message on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    from_chat_id: Unique identifier for the chat where the original message was sent (or username of the target bot, supergroup or channel in the format @username)
    message_id: Message identifier in the chat specified in from_chat_id
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    caption: New caption for media, 0-1024 characters after entities parsing. If not specified, the original caption is kept.
    parse_mode: Mode for parsing entities in the new caption. See formatting options for more details.
    caption_entities: A JSON-serialized list of special entities that appear in the new caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media. Ignored if a new caption isn't specified.
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'from_chat_id': from_chat_id, 'message_id': message_id}
    if message_thread_id is not None:
        payload['message_thread_id'] = message_thread_id
    if caption is not None:
        payload['caption'] = caption
    if parse_mode is not None:
        payload['parse_mode'] = parse_mode
    serialized_caption_entities = _serialize_entities(caption_entities)
    if serialized_caption_entities is not None:
        payload['caption_entities'] = serialized_caption_entities
    if show_caption_above_media is not None:
        payload['show_caption_above_media'] = show_caption_above_media
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if protect_content is not None:
        payload['protect_content'] = protect_content
    serialized_reply = _serialize_reply_parameters(reply_parameters)
    if serialized_reply is not None:
        payload['reply_parameters'] = serialized_reply
    if reply_markup is not None:
        payload['reply_markup'] = serialize_reply_markup(reply_markup)
    result = await self._call('copyMessage', json_body=payload)
    return MessageId.from_dict(result)
