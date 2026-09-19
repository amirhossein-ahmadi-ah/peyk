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

async def delete_all_message_reactions(self, chat_id: Union[int, str], message_id: Optional[int]=None, *, user_id: Optional[int]=None, actor_chat_id: Optional[int]=None) -> bool:
    """Use this method to remove up to 10000 recent reactions in a group or a supergroup chat added by a given user or chat. The bot must have the 'can_delete_messages' administrator right in the chat. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup in the format @username
    message_id: Value accepted by this operation.
    user_id: Identifier of the user whose reactions will be removed, if the reactions were added by a user
    actor_chat_id: Identifier of the chat whose reactions will be removed, if the reactions were added by a chat

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if message_id is not None:
        payload['message_id'] = _serialize_api_value(message_id)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if user_id is not None:
        payload['user_id'] = _serialize_api_value(user_id)
    if actor_chat_id is not None:
        payload['actor_chat_id'] = _serialize_api_value(actor_chat_id)
    result = await self._call('deleteAllMessageReactions', json_body=payload)
    return _parse_api_result('bool', result)
