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

async def answer_inline_query(self, inline_query_id: str, results: Sequence[Union[InlineQueryResult, Mapping[str, object]]], *, cache_time: Optional[int]=None, is_personal: Optional[bool]=None, next_offset: Optional[str]=None, button: Optional[Union[InlineQueryResultsButton, Mapping[str, object]]]=None) -> bool:
    """Use this method to send answers to an inline query. On success, True is returned.
No more than 50 results per query are allowed.

Args:
    inline_query_id: Unique identifier for the answered query
    results: A JSON-serialized Array of results for the inline query
    cache_time: The maximum amount of time in seconds that the result of the inline query may be cached on the server. Defaults to 300.
    is_personal: Pass True if results may be cached on the server side only for the user that sent the query. By default, results may be returned to any user who sends the same query.
    next_offset: Pass the offset that a client should send in the next query with the same text to receive more results. Pass an empty string if there are no more results or if you don't support pagination. Offset length can't exceed 64 bytes.
    button: A JSON-serialized object describing a button to be shown above inline query results

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'inline_query_id': inline_query_id, 'results': [serialize_inline_result(r) for r in results]}
    if cache_time is not None:
        payload['cache_time'] = cache_time
    if is_personal is not None:
        payload['is_personal'] = is_personal
    if next_offset is not None:
        payload['next_offset'] = next_offset
    if button is not None:
        if isinstance(button, InlineQueryResultsButton):
            payload['button'] = button.to_dict()
        else:
            payload['button'] = dict(button)
    return bool(await self._call('answerInlineQuery', json_body=payload))
