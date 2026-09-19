from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]
from ._serialization import _serialize_entities, _serialize_reply_parameters, _serialize_link_preview

async def edit_message_text(self, text: str, *, chat_id: Optional[ChatId]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, parse_mode: Optional[str]=None, entities: Optional[EntitiesInput]=None, link_preview_options: Optional[Union[LinkPreviewOptions, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> Union[Message, bool]:
    """Use this method to edit text, rich and game messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.

Args:
    text: New text of the message, 1-4096 characters after entity parsing; required if rich_message isn't specified
    chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
    message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
    entities: A JSON-serialized list of special entities that appear in message text, which can be specified instead of parse_mode
    link_preview_options: Link preview generation options for the message
    reply_markup: A JSON-serialized object for an inline keyboard

Returns:
    Union[Message, bool]: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'text': text}
    if inline_message_id is not None:
        payload['inline_message_id'] = inline_message_id
    else:
        if chat_id is None or message_id is None:
            raise ValueError('edit_message_text requires chat_id+message_id or inline_message_id')
        payload['chat_id'] = chat_id
        payload['message_id'] = message_id
    if parse_mode is not None:
        payload['parse_mode'] = parse_mode
    serialized_entities = _serialize_entities(entities)
    if serialized_entities is not None:
        payload['entities'] = serialized_entities
    serialized_preview = _serialize_link_preview(link_preview_options)
    if serialized_preview is not None:
        payload['link_preview_options'] = serialized_preview
    if reply_markup is not None:
        payload['reply_markup'] = serialize_reply_markup(reply_markup)
    result = await self._call('editMessageText', json_body=payload)
    if isinstance(result, bool):
        return result
    return Message.from_dict(result)
