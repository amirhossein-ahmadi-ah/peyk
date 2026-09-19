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

async def set_chat_member_tag(self, chat_id: Union[int, str], user_id: int, *, tag: Optional[str]=None) -> bool:
    """Use this method to set a tag for a regular member in a group or a supergroup. The bot must be an administrator in the chat for this to work and must have the can_manage_tags administrator right. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    user_id: Unique identifier of the target user
    tag: New tag for the member; 0-16 characters, emoji are not allowed

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if tag is not None:
        payload['tag'] = _serialize_api_value(tag)
    result = await self._call('setChatMemberTag', json_body=payload)
    return _parse_api_result('bool', result)
