from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def send_live_photo(self, chat_id: ChatId, live_photo: MediaInput, photo: MediaInput, *, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[EntitiesInput]=None, show_caption_above_media: Optional[bool]=None, has_spoiler: Optional[bool]=None, message_thread_id: Optional[int]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> Message:
    """Use this method to send live photos. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target channel (in the format @channelusername)
    live_photo: Live photo video to send. The video must be no longer than 10 seconds and must not exceed 10 MB in size. Pass a file_id as String to send a video that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files. Sending live photos by a URL is currently unsupported.
    photo: The static photo to send. Pass a file_id as String to send a photo that exists on the Telegram servers (recommended) or upload a new video using multipart/form-data. More information on Sending Files. Sending live photos by a URL is currently unsupported.
    caption: Video caption (may also be used when resending videos by file_id), 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the video caption. See formatting options for more details.
    caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media
    has_spoiler: Pass True if the video needs to be covered with a spoiler animation
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    Message: Result returned by Telegram on successful execution."""
    extra: Dict[str, object] = {}
    if show_caption_above_media is not None:
        extra['show_caption_above_media'] = show_caption_above_media
    if has_spoiler is not None:
        extra['has_spoiler'] = has_spoiler
    if isinstance(live_photo, str) and isinstance(photo, str):
        payload: Dict[str, object] = {'chat_id': chat_id, 'live_photo': live_photo, 'photo': photo}
        payload.update(extra)
        self._apply_caption_json(payload, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities)
        self._apply_send_options_json(payload, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
        result = await self._call('sendLivePhoto', json_body=payload)
        return Message.from_dict(result)
    fields: Dict[str, str] = {'chat_id': str(chat_id)}
    files: Dict[str, FilePayload] = {}
    if isinstance(live_photo, str):
        fields['live_photo'] = live_photo
    else:
        files['live_photo'] = self._as_file_payload(live_photo, default_filename='live_photo.mp4')
    if isinstance(photo, str):
        fields['photo'] = photo
    else:
        files['photo'] = self._as_file_payload(photo, default_filename='photo.jpg')
    for key, value in extra.items():
        fields[key] = str(value)
    self._apply_caption_form(fields, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities)
    self._apply_send_options_form(fields, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
    result = await self._call('sendLivePhoto', data=fields, files=files)
    return Message.from_dict(result)
