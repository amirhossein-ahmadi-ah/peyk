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

async def get_user_chat_boosts(self, chat_id: Union[int, str], user_id: int) -> object:
    """Use this method to get the list of boosts added to a chat by a user. Requires administrator rights in the chat. Returns a UserChatBoosts object.

Args:
    chat_id: Unique identifier for the chat or username of the channel in the format @username
    user_id: Unique identifier of the target user"""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    result = await self._call('getUserChatBoosts', json_body=payload)
    return _parse_api_result('UserChatBoosts', result)
