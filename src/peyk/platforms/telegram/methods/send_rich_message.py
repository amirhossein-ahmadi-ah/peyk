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

async def send_rich_message(self, chat_id: Union[int, str], rich_message: Optional[InputRichMessage]=None, *, text: Optional[str]=None, parse_mode: Optional[str]=None, blocks: Optional[object]=None, media: Optional[object]=None, business_connection_id: Optional[str]=None, message_thread_id: Optional[int]=None, direct_messages_topic_id: Optional[int]=None, ephemeral_message_parameters: Optional[EphemeralMessageParameters]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, allow_paid_broadcast: Optional[bool]=None, message_effect_id: Optional[str]=None, suggested_post_parameters: Optional[SuggestedPostParameters]=None, reply_parameters: Optional[ReplyParameters]=None, reply_markup: Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply]]=None) -> Message:
    """Use this method to send rich messages. If the message contains a block with a media element, then the bot must have the right to send the media to the chat. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    rich_message: The message to be sent
    text: Value accepted by this operation.
    parse_mode: Value accepted by this operation.
    blocks: Value accepted by this operation.
    media: Value accepted by this operation.
    business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent. Bot can send rich messages on behalf of a business account only if the corresponding user can send rich messages.
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
    ephemeral_message_parameters: Value accepted by this operation.
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
    message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
    suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_thread_id is not None:
        payload['message_thread_id'] = _serialize_api_value(message_thread_id)
    if direct_messages_topic_id is not None:
        payload['direct_messages_topic_id'] = _serialize_api_value(direct_messages_topic_id)
    if ephemeral_message_parameters is not None:
        payload['ephemeral_message_parameters'] = _serialize_api_value(ephemeral_message_parameters)
    if rich_message is not None:
        payload['rich_message'] = _serialize_api_value(rich_message)
    elif text is not None:
        payload['text'] = _serialize_api_value(text)
        if parse_mode is not None:
            payload['parse_mode'] = _serialize_api_value(parse_mode)
        if blocks is not None:
            payload['blocks'] = _serialize_api_value(blocks)
        if media is not None:
            payload['media'] = _serialize_api_value(media)
    if disable_notification is not None:
        payload['disable_notification'] = _serialize_api_value(disable_notification)
    if protect_content is not None:
        payload['protect_content'] = _serialize_api_value(protect_content)
    if allow_paid_broadcast is not None:
        payload['allow_paid_broadcast'] = _serialize_api_value(allow_paid_broadcast)
    if message_effect_id is not None:
        payload['message_effect_id'] = _serialize_api_value(message_effect_id)
    if suggested_post_parameters is not None:
        payload['suggested_post_parameters'] = _serialize_api_value(suggested_post_parameters)
    if reply_parameters is not None:
        payload['reply_parameters'] = _serialize_api_value(reply_parameters)
    if reply_markup is not None:
        payload['reply_markup'] = _serialize_api_value(reply_markup)
    result = await self._call('sendRichMessage', json_body=payload)
    return _parse_api_result('Message', result)
