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

async def answer_web_app_query(self, web_app_query_id: str, result: InlineQueryResult) -> SentWebAppMessage:
    """Use this method to set the result of an interaction with a Web App and send a corresponding message on behalf of the user to the chat from which the query originated. On success, a SentWebAppMessage object is returned.

Args:
    web_app_query_id: Unique identifier for the query to be answered
    result: A JSON-serialized object describing the message to be sent

Returns:
    SentWebAppMessage: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if web_app_query_id is not None:
        payload['web_app_query_id'] = _serialize_api_value(web_app_query_id)
    if result is not None:
        payload['result'] = _serialize_api_value(result)
    result = await self._call('answerWebAppQuery', json_body=payload)
    return _parse_api_result('SentWebAppMessage', result)
