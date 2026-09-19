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

async def send_rich_message_draft(self, chat_id: int, draft_id: Optional[int]=None, rich_message: Optional[InputRichMessage]=None, *, text: Optional[str]=None, message_thread_id: Optional[int]=None, can_stop: Optional[bool]=None, keep_on_stop: Optional[bool]=None) -> bool:
    """Use this method to stream a partial rich message to a user while the message is being generated. Note that the streamed draft is ephemeral and acts as a temporary 30-second preview - once the output is finalized, you must call sendRichMessage with the complete message to persist it in the user's chat. Returns True on success.

Args:
    chat_id: Unique identifier for the target private chat
    draft_id: Unique identifier of the message draft; must be non-zero. Changes to drafts with the same identifier are animated.
    rich_message: The partial message to be streamed. Direct upload of new files isn't supported.
    text: Value accepted by this operation.
    message_thread_id: Unique identifier for the target message thread
    can_stop: Value accepted by this operation.
    keep_on_stop: Value accepted by this operation.

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_thread_id is not None:
        payload['message_thread_id'] = _serialize_api_value(message_thread_id)
    if draft_id is not None:
        payload['draft_id'] = _serialize_api_value(draft_id)
    if rich_message is not None:
        payload['rich_message'] = _serialize_api_value(rich_message)
    elif text is not None:
        payload['text'] = _serialize_api_value(text)
    if can_stop is not None:
        payload['can_stop'] = _serialize_api_value(can_stop)
    if keep_on_stop is not None:
        payload['keep_on_stop'] = _serialize_api_value(keep_on_stop)
    result = await self._call('sendRichMessageDraft', json_body=payload)
    return _parse_api_result('Message', result)
