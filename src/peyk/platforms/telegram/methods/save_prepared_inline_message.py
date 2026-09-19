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

async def save_prepared_inline_message(self, user_id: int, result: Union[InlineQueryResult, Mapping[str, object]], *, allow_user_chats: Optional[bool]=None, allow_bot_chats: Optional[bool]=None, allow_group_chats: Optional[bool]=None, allow_channel_chats: Optional[bool]=None) -> PreparedInlineMessage:
    """Stores a message that can be sent by a user of a Mini App. Returns a PreparedInlineMessage object.

Args:
    user_id: Unique identifier of the target user that can use the prepared message
    result: A JSON-serialized object describing the message to be sent
    allow_user_chats: Pass True if the message can be sent to private chats with users
    allow_bot_chats: Pass True if the message can be sent to private chats with bots
    allow_group_chats: Pass True if the message can be sent to group and supergroup chats
    allow_channel_chats: Pass True if the message can be sent to channel chats"""
    payload: Dict[str, object] = {'user_id': user_id, 'result': serialize_inline_result(result)}
    if allow_user_chats is not None:
        payload['allow_user_chats'] = allow_user_chats
    if allow_bot_chats is not None:
        payload['allow_bot_chats'] = allow_bot_chats
    if allow_group_chats is not None:
        payload['allow_group_chats'] = allow_group_chats
    if allow_channel_chats is not None:
        payload['allow_channel_chats'] = allow_channel_chats
    return PreparedInlineMessage.from_dict(await self._call('savePreparedInlineMessage', json_body=payload))
