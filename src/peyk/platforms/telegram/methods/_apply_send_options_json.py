from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

from peyk.transport import FilePayload
from ..models import *

ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

from ._serialization import _serialize_entities, _serialize_reply_parameters, _serialize_link_preview

def _apply_send_options_json(self, payload: Dict[str, object], *, message_thread_id: Optional[int]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> None:
    """Telegram Bot API method ``_apply_send_options_json`` (T1-T5).

The implementation is preserves the existing implementation ``TelegramClient``
without changing request construction, return parsing, or error behavior."""
    if message_thread_id is not None:
        payload['message_thread_id'] = message_thread_id
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    if protect_content is not None:
        payload['protect_content'] = protect_content
    serialized_reply = _serialize_reply_parameters(reply_parameters)
    if serialized_reply is not None:
        payload['reply_parameters'] = serialized_reply
    if reply_markup is not None:
        payload['reply_markup'] = serialize_reply_markup(reply_markup)
