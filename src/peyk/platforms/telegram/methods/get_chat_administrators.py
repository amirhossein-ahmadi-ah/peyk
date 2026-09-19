from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def get_chat_administrators(self, chat_id: ChatId, *, return_bots: Optional[bool]=None) -> List[ChatMember]:
    """Use this method to get a list of administrators in a chat. Returns an Array of ChatMember objects.

Args:
    chat_id: Unique identifier for the target chat or username of the target supergroup or channel in the format @username
    return_bots: Pass True to additionally receive all bots that are administrators of the chat. By default, bots other than the current bot are omitted.

Returns:
    List[ChatMember]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id}
    if return_bots is not None:
        payload['return_bots'] = return_bots
    result = await self._call('getChatAdministrators', json_body=payload)
    return [m for m in (parse_chat_member(item) for item in result or []) if m is not None]
