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

async def edit_ephemeral_message_media(self, chat_id: Union[int, str], receiver_user_id: Optional[int]=None, ephemeral_message_id: Optional[int]=None, media: Optional[InputMedia]=None, *, reply_markup: Optional[InlineKeyboardMarkup]=None) -> bool:
    """Use this method to edit the media of an ephemeral message. Note that it is not guaranteed that the user will receive the message edit event, especially if they are offline. On success, True is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    receiver_user_id: Identifier of the user who received the message
    ephemeral_message_id: Identifier of the ephemeral message to edit
    media: A JSON-serialized object for the new media content of the message. A new file can't be uploaded; use a previously uploaded file via its file_id or specify a URL.
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
    if media is not None:
        payload['media'] = _serialize_api_value(media)
    if reply_markup is not None:
        payload['reply_markup'] = _serialize_api_value(reply_markup)
    result = await self._call('editEphemeralMessageMedia', json_body=payload)
    return _parse_api_result('Message', result)
