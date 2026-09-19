from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def stop_message_live_location(self, *, chat_id: Optional[ChatId]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, reply_markup: Optional[ReplyMarkup]=None) -> Union[Message, bool]:
    """Use this method to stop updating a live location message before live_period expires. On success, if the message is not an inline message, the edited Message is returned, otherwise True is returned.

Args:
    chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
    message_id: Required if inline_message_id is not specified. Identifier of the message with live location to stop.
    inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    reply_markup: A JSON-serialized object for a new inline keyboard

Returns:
    Union[Message, bool]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = self._edit_target(chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, method='stop_message_live_location')
    if reply_markup is not None:
        payload['reply_markup'] = serialize_reply_markup(reply_markup)
    result = await self._call('stopMessageLiveLocation', json_body=payload)
    if isinstance(result, bool):
        return result
    return Message.from_dict(result)
