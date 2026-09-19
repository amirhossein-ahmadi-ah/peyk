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

async def send_chat_join_request_web_app(self, chat_join_request_query_id: Optional[str]=None, web_app_url: Optional[str]=None, *, chat_id: Optional[int]=None, user_id: Optional[int]=None, query_id: Optional[str]=None) -> bool:
    """Use this method to process a received chat join request query by showing a Mini App to the user before deciding the outcome. Call answerChatJoinRequestQuery to resolve the join request query based on the user interaction with the Mini App. Returns True on success.

Args:
    chat_join_request_query_id: Unique identifier of the join request query
    web_app_url: An HTTPS URL of a Web App to be opened with additional data as specified in Initializing Web Apps
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
    if web_app_url is not None:
        payload['web_app_url'] = _serialize_api_value(web_app_url)
    result = await self._call('sendChatJoinRequestWebApp', json_body=payload)
    return _parse_api_result('bool', result)
