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

async def send_game(self, chat_id: Union[int, str], game_short_name: str, *, business_connection_id: Optional[str]=None, message_thread_id: Optional[int]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, allow_paid_broadcast: Optional[bool]=None, message_effect_id: Optional[str]=None, reply_parameters: Optional[ReplyParameters]=None, reply_markup: Optional[InlineKeyboardMarkup]=None) -> Message:
    """Use this method to send a game. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot in the format @username. Games can't be sent to channel direct messages chats and channel chats.
    game_short_name: Short name of the game, serves as the unique identifier for the game. Set up your games via @BotFather.
    business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
    message_effect_id: Unique identifier of the message effect to be added to the message; for private chats only
    reply_parameters: Description of the message to reply to
    reply_markup: A JSON-serialized object for an inline keyboard. If empty, one 'Play game_title' button will be shown. If not empty, the first button must launch the game.

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_thread_id is not None:
        payload['message_thread_id'] = _serialize_api_value(message_thread_id)
    if game_short_name is not None:
        payload['game_short_name'] = _serialize_api_value(game_short_name)
    if disable_notification is not None:
        payload['disable_notification'] = _serialize_api_value(disable_notification)
    if protect_content is not None:
        payload['protect_content'] = _serialize_api_value(protect_content)
    if allow_paid_broadcast is not None:
        payload['allow_paid_broadcast'] = _serialize_api_value(allow_paid_broadcast)
    if message_effect_id is not None:
        payload['message_effect_id'] = _serialize_api_value(message_effect_id)
    if reply_parameters is not None:
        payload['reply_parameters'] = _serialize_api_value(reply_parameters)
    if reply_markup is not None:
        payload['reply_markup'] = _serialize_api_value(reply_markup)
    result = await self._call('sendGame', json_body=payload)
    return _parse_api_result('Message', result)
