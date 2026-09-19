from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]
from ._serialization import _serialize_entities, _serialize_reply_parameters, _serialize_link_preview

async def send_message(self, chat_id: ChatId, text: str, *, business_connection_id: Optional[str]=None, message_thread_id: Optional[int]=None, parse_mode: Optional[str]=None, entities: Optional[EntitiesInput]=None, link_preview_options: Optional[Union[LinkPreviewOptions, Mapping[str, object]]]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> Message:
    """Use this method to send text messages. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    text: Text of the message to be sent, 1-4096 characters after entities parsing
    business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
    entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
    link_preview_options: Link preview generation options for the message
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'text': text}
    if business_connection_id is not None:
        payload['business_connection_id'] = business_connection_id
    if message_thread_id is not None:
        payload['message_thread_id'] = message_thread_id
    if parse_mode is not None:
        payload['parse_mode'] = parse_mode
    serialized_entities = _serialize_entities(entities)
    if serialized_entities is not None:
        payload['entities'] = serialized_entities
    serialized_preview = _serialize_link_preview(link_preview_options)
    if serialized_preview is not None:
        payload['link_preview_options'] = serialized_preview
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if protect_content is not None:
        payload['protect_content'] = protect_content
    serialized_reply = _serialize_reply_parameters(reply_parameters)
    if serialized_reply is not None:
        payload['reply_parameters'] = serialized_reply
    if reply_markup is not None:
        payload['reply_markup'] = serialize_reply_markup(reply_markup)
    result = await self._call('sendMessage', json_body=payload)
    return Message.from_dict(result)
