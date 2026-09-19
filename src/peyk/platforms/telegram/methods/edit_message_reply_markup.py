from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def edit_message_reply_markup(self, *, chat_id: Optional[ChatId]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, reply_markup: Optional[ReplyMarkup]=None) -> Union[Message, bool]:
    """Use this method to edit only the reply markup of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.

Args:
    chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
    message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    reply_markup: A JSON-serialized object for an inline keyboard

Returns:
    Union[Message, bool]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if inline_message_id is not None:
        payload['inline_message_id'] = inline_message_id
    else:
        if chat_id is None or message_id is None:
            raise ValueError('edit_message_reply_markup requires chat_id+message_id or inline_message_id')
        payload['chat_id'] = chat_id
        payload['message_id'] = message_id
    if reply_markup is not None:
        payload['reply_markup'] = serialize_reply_markup(reply_markup)
    result = await self._call('editMessageReplyMarkup', json_body=payload)
    if isinstance(result, bool):
        return result
    return Message.from_dict(result)
