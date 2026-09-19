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

async def answer_chat_join_request_query(self, chat_join_request_query_id: Optional[str]=None, result: Optional[str]=None, *, chat_id: Optional[int]=None, user_id: Optional[int]=None, query_id: Optional[str]=None) -> bool:
    """Use this method to process a received chat join request query. Returns True on success.

Args:
    chat_join_request_query_id: Unique identifier of the join request query
    result: Result of the query. Must be either 'approve' to allow the user to join the chat, 'decline' to disallow the user to join the chat, or 'queue' to leave the decision to other administrators.
    chat_id: Value accepted by this operation.
    user_id: Value accepted by this operation.
    query_id: Value accepted by this operation.

Returns:
    bool: Result returned by Telegram on successful execution."""
    if chat_join_request_query_id is None:
        chat_join_request_query_id = query_id
    payload: Dict[str, object] = {}
    if chat_join_request_query_id is not None:
        payload['chat_join_request_query_id'] = _serialize_api_value(chat_join_request_query_id)
    if result is not None:
        payload['result'] = _serialize_api_value(result)
    result = await self._call('answerChatJoinRequestQuery', json_body=payload)
    return _parse_api_result('bool', result)
