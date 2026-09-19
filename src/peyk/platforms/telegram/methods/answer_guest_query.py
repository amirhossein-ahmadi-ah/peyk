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

async def answer_guest_query(self, guest_query_id: str, result: InlineQueryResult) -> SentGuestMessage:
    """Use this method to reply to a received guest message. On success, a SentGuestMessage object is returned.

Args:
    guest_query_id: Unique identifier for the query to be answered
    result: A JSON-serialized object describing the message to be sent

Returns:
    SentGuestMessage: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if guest_query_id is not None:
        payload['guest_query_id'] = _serialize_api_value(guest_query_id)
    if result is not None:
        payload['result'] = _serialize_api_value(result)
    result = await self._call('answerGuestQuery', json_body=payload)
    return _parse_api_result('SentGuestMessage', result)
