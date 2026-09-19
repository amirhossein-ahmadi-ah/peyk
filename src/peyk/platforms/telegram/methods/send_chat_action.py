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

async def send_chat_action(self, chat_id: Union[int, str], action: str, *, business_connection_id: Optional[str]=None, message_thread_id: Optional[int]=None) -> bool:
    """Use this method when you need to tell the user that something is happening on the bot's side. The status is set for 5 seconds or less (when a message arrives from your bot, Telegram clients clear its typing status). Returns True on success.
Example: The ImageBot needs some time to process a request and upload the image. Instead of sending a text message along the lines of 'Retrieving image, please wait…', the bot may use sendChatAction with action = upload_photo. The user will see a 'sending photo' status for the bot.
We only recommend using this method when a response from the bot will take a noticeable amount of time to arrive.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot or supergroup in the format @username. Channel chats and channel direct messages chats aren't supported.
    action: Type of action to broadcast. Choose one, depending on what the user is about to receive: typing for text messages, upload_photo for photos, record_video or upload_video for videos, record_voice or upload_voice for voice notes, upload_document for general files, choose_sticker for stickers, find_location for location data, record_video_note or upload_video_note for video notes.
    business_connection_id: Unique identifier of the business connection on behalf of which the action will be sent
    message_thread_id: Unique identifier for the target message thread or topic of a forum; for supergroups and private chats of bots with forum topic mode enabled only

Returns:
    bool: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {}
    if business_connection_id is not None:
        payload['business_connection_id'] = _serialize_api_value(business_connection_id)
    if chat_id is not None:
        payload['chat_id'] = _serialize_api_value(chat_id)
    if message_thread_id is not None:
        payload['message_thread_id'] = _serialize_api_value(message_thread_id)
    if action is not None:
        payload['action'] = _serialize_api_value(action)
    result = await self._call('sendChatAction', json_body=payload)
    return _parse_api_result('bool', result)
