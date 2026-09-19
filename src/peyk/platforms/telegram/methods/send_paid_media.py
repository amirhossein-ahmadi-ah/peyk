from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
import orjson
from peyk.transport import FilePayload
from ..errors import TelegramAPIError, ResponseParameters
from ..models import *
from .. import models as _models
globals().update({k: v for k, v in vars(_models).items() if k.startswith('_')})
from peyk.platforms.telegram.methods._serialization import _serialize_entities
from peyk.platforms.telegram.methods._serialization import _serialize_reply_parameters
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def send_paid_media(self, chat_id: Union[int, str], star_count: int, media: List[object], *, business_connection_id: Optional[str]=None, message_thread_id: Optional[int]=None, direct_messages_topic_id: Optional[int]=None, payload: Optional[str]=None, caption: Optional[str]=None, parse_mode: Optional[str]=None, caption_entities: Optional[List[MessageEntity]]=None, show_caption_above_media: Optional[bool]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, allow_paid_broadcast: Optional[bool]=None, suggested_post_parameters: Optional[object]=None, reply_parameters: Optional[ReplyParameters]=None, reply_markup: Optional[object]=None) -> Message:
    """Use this method to send paid media. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username. If the chat is a channel, all Telegram Star proceeds from this media will be credited to the chat's balance. Otherwise, they will be credited to the bot's balance.
    star_count: The number of Telegram Stars that must be paid to buy access to the media; 1-25000
    media: A JSON-serialized Array describing the media to be sent; up to 10 items
    business_connection_id: Unique identifier of the business connection on behalf of which the message will be sent
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    direct_messages_topic_id: Identifier of the direct messages topic to which the message will be sent; required if the message is sent to a direct messages chat
    payload: Bot-defined paid media payload, 0-128 bytes. This will not be displayed to the user, use it for your internal processes.
    caption: Media caption, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the media caption. See formatting options for more details.
    caption_entities: A JSON-serialized list of special entities that appear in the caption, which can be specified instead of parse_mode
    show_caption_above_media: Pass True if the caption must be shown above the message media
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding and saving
    allow_paid_broadcast: Pass True to allow up to 1000 messages per second, ignoring broadcasting limits for a fee of 0.1 Telegram Stars per message. The relevant Stars will be withdrawn from the bot's balance.
    suggested_post_parameters: A JSON-serialized object containing the parameters of the suggested post to send; for direct messages chats only. If the message is sent as a reply to another suggested post, then that suggested post is automatically declined.
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    Message: Result returned by Telegram on successful execution."""
    files: Dict[str, FilePayload] = {}

    def resolve_item(item: object, index: int) -> Dict[str, object]:
        """Executes the resolve_item operation.
                
                Args:
                    item: Value of the declared parameter type.
                    index: Value of the declared parameter type.
                
                
                Returns:
                    The operation result (``Dict[str, object]``).
                
        
        Raises:
            TypeError: Raised when the operation cannot complete.
        """
        raw = _serialize_api_value(item)
        if not isinstance(raw, dict):
            raise TypeError(f'unsupported paid media item: {type(item).__name__}')
        for attr in ('media', 'photo', 'thumbnail', 'cover'):
            if not hasattr(item, attr):
                continue
            value = getattr(item, attr)
            if value is None:
                continue
            if self._is_upload(value):
                suffix = 'paid_media' if attr == 'media' else f'{attr}_paid_media'
                name = f'file{index}_{suffix}'
                files[name] = self._as_file_payload(value, default_filename=f'{suffix}_{index}')
                raw[attr] = f'attach://{name}'
            else:
                raw[attr] = value
        return raw
    media_payload = [resolve_item(item, index) for index, item in enumerate(media)]
    common = {'business_connection_id': business_connection_id, 'chat_id': chat_id, 'message_thread_id': message_thread_id, 'direct_messages_topic_id': direct_messages_topic_id, 'star_count': star_count, 'payload': payload, 'caption': caption, 'parse_mode': parse_mode, 'caption_entities': _serialize_entities(caption_entities), 'show_caption_above_media': show_caption_above_media, 'disable_notification': disable_notification, 'protect_content': protect_content, 'allow_paid_broadcast': allow_paid_broadcast, 'suggested_post_parameters': suggested_post_parameters, 'reply_parameters': _serialize_reply_parameters(reply_parameters), 'reply_markup': reply_markup}
    common = {k: v for k, v in common.items() if v is not None}
    if files:
        fields: Dict[str, str] = {}
        for key, value in common.items():
            fields[key] = self._json_field(value) if key in {'media', 'caption_entities', 'suggested_post_parameters', 'reply_parameters', 'reply_markup'} else str(value)
        fields['media'] = self._json_field(media_payload)
        result = await self._call('sendPaidMedia', data=fields, files=files)
    else:
        common['media'] = media_payload
        result = await self._call('sendPaidMedia', json_body=common)
    return Message.from_dict(result)
