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

async def get_game_high_scores(self, user_id: int, *, chat_id: Optional[int]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None) -> List[GameHighScore]:
    """Use this method to get data for high score tables. Will return the score of the specified user and several of their neighbors in a game. Returns an Array of GameHighScore objects.
This method will currently return scores for the target user, plus two of their closest neighbors on each side. Will also return the top three users if the user and their neighbors are not among them. Please note that this behavior is subject to change.

Args:
    user_id: Target user id
    chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat.
    message_id: Required if inline_message_id is not specified. Identifier of the sent message.
    inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.

Returns:
    List[GameHighScore]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_id is not None:
        payload['message_id'] = _serialize_api_value(message_id)
    if inline_message_id is not None:
        payload['inline_message_id'] = _serialize_api_value(inline_message_id)
    result = await self._call('getGameHighScores', json_body=payload)
    return _parse_api_result('List[GameHighScore]', result)
