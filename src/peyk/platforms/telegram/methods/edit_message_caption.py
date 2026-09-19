from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]
from ._serialization import _serialize_entities, _serialize_reply_parameters, _serialize_link_preview

async def edit_message_caption(self, *, chat_id: Optional[ChatId]=None, message_id: Optional[int]=None, inline_message_id: Optional[str]=None, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[EntitiesInput]=None, show_caption_above_media: Optional[bool]=None, reply_markup: Optional[ReplyMarkup]=None) -> Union[Message, bool]:
    """Use this method to edit captions of messages. On success, if the edited message is not an inline message, the edited Message is returned, otherwise True is returned. Note that business messages that were not sent by the bot and do not contain an inline keyboard can only be edited within 48 hours from the time they were sent.

Args:
    chat_id: Required if inline_message_id is not specified. Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username.
    message_id: Required if inline_message_id is not specified. Identifier of the message to edit.
    inline_message_id: Required if chat_id and message_id are not specified. Identifier of the inline message.
    caption: New caption of the message, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the message caption. See formatting options for more details.
    caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media. Supported only for animation, photo and video messages.
    reply_markup: A JSON-serialized object for an inline keyboard

Returns:
    Union[Message, bool]: Result returned by Telegram on successful execution."""
    target = self._edit_target(chat_id=chat_id, message_id=message_id, inline_message_id=inline_message_id, method='edit_message_caption')
    payload: Dict[str, object] = dict(target)
    if caption is not None:
        payload['caption'] = caption
    if parse_mode is not None:
        payload['parse_mode'] = parse_mode
    serialized = _serialize_entities(caption_entities)
    if serialized is not None:
        payload['caption_entities'] = serialized
    if show_caption_above_media is not None:
        payload['show_caption_above_media'] = show_caption_above_media
    if reply_markup is not None:
        payload['reply_markup'] = serialize_reply_markup(reply_markup)
    result = await self._call('editMessageCaption', json_body=payload)
    if isinstance(result, bool):
        return result
    return Message.from_dict(result)
