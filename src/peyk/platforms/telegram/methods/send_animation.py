from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def send_animation(self, chat_id: ChatId, animation: MediaInput, *, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[EntitiesInput]=None, show_caption_above_media: Optional[bool]=None, has_spoiler: Optional[bool]=None, duration: Optional[int]=None, width: Optional[int]=None, height: Optional[int]=None, thumbnail: Optional[MediaInput]=None, message_thread_id: Optional[int]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> Message:
    """Use this method to send animation files (GIF or H.264/MPEG-4 AVC video without sound). On success, the sent Message is returned. Bots can currently send animation files of up to 50 MB in size, this limit may be changed in the future.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    animation: Animation to send. Pass a file_id as String to send an animation that exists on the Telegram servers (recommended), pass an HTTP URL as a String for Telegram to get an animation from the Internet, or upload a new animation using multipart/form-data. More information on Sending Files
    caption: Animation caption (may also be used when resending animation by file_id), 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the animation caption. See formatting options for more details.
    caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media
    has_spoiler: Pass True if the animation needs to be covered with a spoiler animation
    duration: Duration of sent animation in seconds
    width: Animation width
    height: Animation height
    thumbnail: Thumbnail of the file sent; can be ignored if thumbnail generation for the file is supported server-side. The thumbnail should be in JPEG format and less than 200 kB in size. A thumbnail's width and height should not exceed 320. Ignored if the file is not uploaded using multipart/form-data. Thumbnails can't be reused and can be only uploaded as a new file, so you can pass 'attach://' if the thumbnail was uploaded using multipart/form-data under . More information on Sending Files
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
    if duration is not None:
        extra['duration'] = duration
    if width is not None:
        extra['width'] = width
    if height is not None:
        extra['height'] = height
    files = {'thumbnail': thumbnail} if thumbnail is not None else None
    return await self._send_file_message('sendAnimation', 'animation', chat_id, animation, caption=caption, parse_mode=parse_mode, caption_entities=caption_entities, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup, extra_json=extra, extra_files=files, default_filename='animation.gif')
