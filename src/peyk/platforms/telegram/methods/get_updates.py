from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def get_updates(self, *, offset: Optional[int]=None, limit: Optional[int]=None, timeout: Optional[int]=None, allowed_updates: Optional[List[str]]=None) -> List[Update]:
    """Use this method to receive incoming updates using long polling (wiki). Returns an Array of Update objects.
Notes
1. This method will not work if an outgoing webhook is set up.
2. In order to avoid getting duplicate updates, recalculate offset after each server response.

Args:
    offset: Identifier of the first update to be returned. Must be greater by one than the highest among the identifiers of previously received updates. By default, updates starting with the earliest unconfirmed update are returned. An update is considered confirmed as soon as getUpdates is called with an offset higher than its update_id. The negative offset can be specified to retrieve updates starting from -offset update from the end of the updates queue. All previous updates will be forgotten.
    limit: Limits the number of updates to be retrieved. Values between 1-100 are accepted. Defaults to 100.
    timeout: Timeout in seconds for long polling. Defaults to 0, i.e. usual short polling. Should be positive, short polling should be used for testing purposes only.
    allowed_updates: A JSON-serialized list of the update types you want your bot to receive. For example, specify ["message", "edited_channel_post", "callback_query"] to only receive updates of these types. See Update for a complete list of available update types. Specify an empty list to receive all update types except chat_member, message_reaction, and message_reaction_count (default). If not specified, the previous setting will be used.

Please note that this parameter doesn't affect updates created before the call to getUpdates, so unwanted updates may be received for a short period of time.

Returns:
    List[Update]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if offset is not None:
        payload['offset'] = offset
    if limit is not None:
        payload['limit'] = limit
    if timeout is not None:
        payload['timeout'] = timeout
    if allowed_updates is not None:
        payload['allowed_updates'] = allowed_updates
    result = await self._call('getUpdates', json_body=payload)
    return Update.list_from_result(result)
