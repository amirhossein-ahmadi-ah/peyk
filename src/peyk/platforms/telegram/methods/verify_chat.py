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

async def verify_chat(self, chat_id: Union[int, str], *, custom_description: Optional[str]=None) -> bool:
    """Verifies a chat on behalf of the organization which is represented by the bot. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username. Channel direct messages chats can't be verified.
    custom_description: Custom description for the verification; 0-70 characters. Must be empty if the organization isn't allowed to provide a custom verification description.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if custom_description is not None:
        payload['custom_description'] = _serialize_api_value(custom_description)
    result = await self._call('verifyChat', json_body=payload)
    return _parse_api_result('bool', result)
