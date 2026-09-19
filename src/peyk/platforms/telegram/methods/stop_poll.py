from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def stop_poll(self, chat_id: ChatId, message_id: int, *, reply_markup: Optional[ReplyMarkup]=None) -> Poll:
    """Use this method to stop a poll which was sent by the bot. On success, the stopped Poll is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    message_id: Identifier of the original message with the poll
    reply_markup: A JSON-serialized object for a new message inline keyboard

Returns:
    Poll: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id, 'message_id': message_id}
    if reply_markup is not None:
        payload['reply_markup'] = serialize_reply_markup(reply_markup)
    result = await self._call('stopPoll', json_body=payload)
    return Poll.from_dict(result)
