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

async def edit_ephemeral_message_caption(self, chat_id: Union[int, str], receiver_user_id: Optional[int]=None, ephemeral_message_id: Optional[int]=None, *, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[List[MessageEntity]]=None, show_caption_above_media: Optional[bool]=None, reply_markup: Optional[InlineKeyboardMarkup]=None) -> bool:
    """Use this method to edit the caption of an ephemeral message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    receiver_user_id: Identifier of the user who received the message
    ephemeral_message_id: Identifier of the ephemeral message to edit
    caption: New caption of the message, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the message caption. See formatting options for more details.
    caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Value accepted by this operation.
    reply_markup: A JSON-serialized object for an inline keyboard

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if receiver_user_id is not None:
        payload['receiver_user_id'] = _serialize_api_value(receiver_user_id)
    if ephemeral_message_id is not None:
        payload['ephemeral_message_id'] = _serialize_api_value(ephemeral_message_id)
    if caption is not None:
        payload['caption'] = _serialize_api_value(caption)
    if parse_mode is not None:
        payload['parse_mode'] = _serialize_api_value(parse_mode)
    if caption_entities is not None:
        payload['caption_entities'] = _serialize_api_value(caption_entities)
    if show_caption_above_media is not None:
        payload['show_caption_above_media'] = _serialize_api_value(show_caption_above_media)
    if reply_markup is not None:
        payload['reply_markup'] = _serialize_api_value(reply_markup)
    result = await self._call('editEphemeralMessageCaption', json_body=payload)
    return _parse_api_result('Message', result)
