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

async def send_gift(self, gift_id: str, *, user_id: Optional[int]=None, chat_id: Optional[Union[int, str]]=None, pay_for_upgrade: Optional[bool]=None, text: Optional[str]=None, text_parse_mode: Optional[str]=None, text_entities: Optional[List[MessageEntity]]=None) -> bool:
    """Sends a gift to the given user or channel chat. The gift can't be converted to Telegram Stars by the receiver. Returns True on success.

Args:
    gift_id: Identifier of the gift; limited gifts can't be sent to channel chats
    user_id: Required if chat_id is not specified. Unique identifier of the target user who will receive the gift.
    chat_id: Required if user_id is not specified. Unique identifier for the chat or username of the channel (in the format @username) that will receive the gift.
    pay_for_upgrade: Pass True to pay for the gift upgrade from the bot's balance, thereby making the upgrade free for the receiver
    text: Text that will be shown along with the gift; 0-128 characters
    text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Entities other than 'bold', 'italic', 'underline', 'strikethrough', 'spoiler', 'custom_emoji', and 'date_time' are ignored.
    text_entities: A JSON-serialized list of special entities that appear in the gift text. It can be specified instead of text_parse_mode. Entities other than 'bold', 'italic', 'underline', 'strikethrough', 'spoiler', 'custom_emoji', and 'date_time' are ignored.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if gift_id is not None:
        payload['gift_id'] = _serialize_api_value(gift_id)
    if pay_for_upgrade is not None:
        payload['pay_for_upgrade'] = _serialize_api_value(pay_for_upgrade)
    if text is not None:
        payload['text'] = _serialize_api_value(text)
    if text_parse_mode is not None:
        payload['text_parse_mode'] = _serialize_api_value(text_parse_mode)
    if text_entities is not None:
        payload['text_entities'] = _serialize_api_value(text_entities)
    result = await self._call('sendGift', json_body=payload)
    return _parse_api_result('bool', result)
