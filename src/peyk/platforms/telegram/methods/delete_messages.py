from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def delete_messages(self, chat_id: ChatId, message_ids: Sequence[int]) -> bool:
    """Use this method to delete multiple messages simultaneously. If some of the specified messages can't be found, they are skipped. Returns True on success.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    message_ids: A JSON-serialized list of 1-100 identifiers of messages to delete. See deleteMessage for limitations on which messages can be deleted.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload = {'chat_id': chat_id, 'message_ids': list(message_ids)}
    return bool(await self._call('deleteMessages', json_body=payload))
