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

async def get_user_personal_chat_messages(self, user_id: int, limit: Optional[int]=None) -> List[Message]:
    """Use this method to get the last messages from the personal chat (i.e., the chat currently added to their profile) of a given user. On success, an Array of Message objects is returned.

Args:
    user_id: Unique identifier for the target user
    limit: The maximum number of messages to return; 1-20

Returns:
    List[Message]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if limit is not None:
        payload['limit'] = _serialize_api_value(limit)
    result = await self._call('getUserPersonalChatMessages', json_body=payload)
    return _parse_api_result('List[Message]', result)
