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

async def send_sticker(self, chat_id: ChatId, sticker: MediaInput, *, message_thread_id: Optional[int]=None, emoji: Optional[str]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> Message:
    """Use this method to send static .WEBP, animated .TGS, or video .WEBM stickers. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    sticker: Sticker to send. Pass a file_id as String to send a file that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get a .WEBP sticker from the Internet, or upload a new .WEBP, .TGS, or .WEBM sticker using multipart/form-data. More information on Sending Files. Video and animated stickers can't be sent via an HTTP URL.
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    emoji: Emoji associated with the sticker; only for just uploaded stickers
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    Message: Result returned by Telegram on successful execution."""
    if not self._is_upload(sticker):
        payload: Dict[str, object] = {'chat_id': chat_id, 'sticker': sticker}
        if emoji is not None:
            payload['emoji'] = emoji
        self._apply_send_options_json(payload, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
        result = await self._call('sendSticker', json_body=payload)
        return Message.from_dict(result)
    fields: Dict[str, str] = {'chat_id': str(chat_id)}
    if emoji is not None:
        fields['emoji'] = emoji
    self._apply_send_options_form(fields, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
    files: Dict[str, FilePayload] = {'sticker': self._as_file_payload(sticker, default_filename='sticker.webp')}
    result = await self._call('sendSticker', data=fields, files=files)
    return Message.from_dict(result)
