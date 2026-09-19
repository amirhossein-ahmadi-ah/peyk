from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def send_file(self, chat_id: str, file_id: str, *, text: Optional[str]=None, chat_keypad: Optional[Union[Keypad, Dict[str, object]]]=None, inline_keypad: Optional[Union[Keypad, Dict[str, object]]]=None, chat_keypad_type: Optional[str]=None, reply_to_message_id: Optional[str]=None, disable_notification: Optional[bool]=None) -> Message:
    """Sends file through the Rubika API.

Args:
    chat_id: Identifier of the target chat.
    file_id: Identifier of the file.
    text: Text content supplied to the operation.
    chat_keypad: Value used by this operation.
    inline_keypad: Value used by this operation.
    chat_keypad_type: Value used by this operation.
    reply_to_message_id: Value used by this operation.
    disable_notification: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
    '"""Rubika client operation ``send_file``.\n\nArgs:\n    chat_id: Value accepted by this operation.\n    file_id: Value accepted by this operation.\n    text: Value accepted by this operation.\n    chat_keypad: Value accepted by this operation.\n    inline_keypad: Value accepted by this operation.\n    chat_keypad_type: Value accepted by this operation.\n    reply_to_message_id: Value accepted by this operation.\n    disable_notification: Value accepted by this operation.\n\nReturns:\n    Message: The value returned by the Rubika API or the local helper.\n\nRaises:\n    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.\n"""'
    payload: Dict[str, object] = {'chat_id': chat_id, 'file_id': file_id}
    if text is not None:
        payload['text'] = text
    kp = self._keypad_to_dict(chat_keypad)
    if kp is not None:
        payload['chat_keypad'] = kp
    ikp = self._keypad_to_dict(inline_keypad)
    if ikp is not None:
        payload['inline_keypad'] = ikp
    if chat_keypad_type is not None:
        payload['chat_keypad_type'] = chat_keypad_type
    if reply_to_message_id is not None:
        payload['reply_to_message_id'] = reply_to_message_id
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    data = await self._call('sendFile', json_body=payload)
    return self._parse_message_id_response(data, 'sendFile')
