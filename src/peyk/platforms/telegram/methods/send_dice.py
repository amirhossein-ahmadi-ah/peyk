from __future__ import annotations
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from peyk.transport import FilePayload
from ..models import *
ChatId = Union[int, str]
EntitiesInput = Sequence[Union[MessageEntity, Mapping[str, object]]]
MediaInput = Union[str, bytes, FilePayload]

async def send_dice(self, chat_id: ChatId, *, message_thread_id: Optional[int]=None, emoji: Optional[str]=None, disable_notification: Optional[bool]=None, protect_content: Optional[bool]=None, reply_parameters: Optional[Union[ReplyParameters, Mapping[str, object]]]=None, reply_markup: Optional[ReplyMarkup]=None) -> Message:
    """Use this method to send an animated emoji that will display a random value. On success, the sent Message is returned.

Args:
    chat_id: Unique identifier for the target chat or username of the target bot, supergroup or channel in the format @username
    message_thread_id: Unique identifier for the target message thread (topic) of a forum; for forum supergroups and private chats of bots with forum topic mode enabled only
    emoji: Emoji on which the dice throw animation is based. Currently, must be one of '', '', '', '', '', or ''. Dice can have values 1-6 for '', '' and '', values 1-5 for '' and '', and values 1-64 for ''. Defaults to ''.
    disable_notification: Sends the message silently. Users will receive a notification with no sound.
    protect_content: Protects the contents of the sent message from forwarding
    reply_parameters: Description of the message to reply to
    reply_markup: Additional interface options. A JSON-serialized object for an inline keyboard, custom reply keyboard, instructions to remove a reply keyboard or to force a reply from the user.

Returns:
    Message: Result returned by Telegram on successful execution."""
    payload: Dict[str, object] = {'chat_id': chat_id}
    if emoji is not None:
        payload['emoji'] = emoji
    self._apply_send_options_json(payload, message_thread_id=message_thread_id, disable_notification=disable_notification, protect_content=protect_content, reply_parameters=reply_parameters, reply_markup=reply_markup)
    result = await self._call('sendDice', json_body=payload)
    return Message.from_dict(result)
