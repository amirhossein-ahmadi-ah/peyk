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

async def set_game_score(self, user_id: int, score: int, *, force: Optional[bool]=None, disable_edit_message: Optional[bool]=None, chat_id: Optional[int]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None) -> Union[Message, bool]:
    """Use this method to set the score of the specified user in a game message. On success, if the message is not an inline message, the Message is returned, otherwise True is returned. Returns an error, if the new score is not greater than the user's current score in the chat and force is False.

Args:
    user_id: User identifier
    score: New score, must be non-negative
    force: Pass True if the high score is allowed to decrease. This can be useful when fixing mistakes or banning cheaters.
    disable_edit_message: Pass True if the game message should not be automatically edited to include the current scoreboard
    chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
    message_id: Required if inline_message_id is not specified. Identifier of the sent message.
    inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.

Returns:
    Union[Message, bool]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if score is not None:
        payload['score'] = _serialize_api_value(score)
    if force is not None:
        payload['force'] = _serialize_api_value(force)
    if disable_edit_message is not None:
        payload['disable_edit_message'] = _serialize_api_value(disable_edit_message)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_id is not None:
        payload['message_id'] = _serialize_api_value(message_id)
    if inline_message_id is not None:
        payload['inline_message_id'] = _serialize_api_value(inline_message_id)
    result = await self._call('setGameScore', json_body=payload)
    return _parse_api_result('Message', result)
