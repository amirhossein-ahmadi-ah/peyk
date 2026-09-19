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

async def set_managed_bot_access_settings(self, user_id: Optional[int]=None, is_access_restricted: Optional[bool]=None, *, added_user_ids: Optional[List[int]]=None, chat_id: Optional[int]=None) -> bool:
    """Use this method to change the access settings of a managed bot. Returns True on success.

Args:
    user_id: User identifier of the managed bot whose access settings will be changed
    is_access_restricted: Pass True if only selected users can access the bot. The bot's owner can always access it.
    added_user_ids: A JSON-serialized list of up to 10 identifiers of users who will have access to the bot in addition to its owner. Ignored if is_access_restricted is False.
    chat_id: Value accepted by this operation.

Returns:
    bool: Result returned by Telegram on successful execution."""
    if user_id is None:
        user_id = chat_id
    payload: Dict[str, object] = {}
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if is_access_restricted is not None:
        payload['is_access_restricted'] = _serialize_api_value(is_access_restricted)
    if added_user_ids is not None:
        payload['added_user_ids'] = _serialize_api_value(added_user_ids)
    result = await self._call('setManagedBotAccessSettings', json_body=payload)
    return _parse_api_result('bool', result)
