from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def forward_message(self, from_chat_id: str, message_id: str, to_chat_id: str, *, disable_notification: Optional[bool]=None) -> str:
    """Performs the forward message operation for the Rubika client.

Args:
    from_chat_id: Value used by this operation.
    message_id: Identifier of the target message.
    to_chat_id: Value used by this operation.
    disable_notification: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
    'Forward a message; returns the new message id.\n    \n    Args:\n        from_chat_id: Value of the declared parameter type.\n        message_id: Value of the declared parameter type.\n        to_chat_id: Value of the declared parameter type.\n        disable_notification: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``str``).\n    '
    payload: Dict[str, object] = {'from_chat_id': from_chat_id, 'message_id': message_id, 'to_chat_id': to_chat_id}
    if disable_notification is not None:
        payload['disable_notification'] = disable_notification
    data = await self._call('forwardMessage', json_body=payload)
    if isinstance(data, dict):
        return str(data.get('new_message_id', ''))
    return ''
