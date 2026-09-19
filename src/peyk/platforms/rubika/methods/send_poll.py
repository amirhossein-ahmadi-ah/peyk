from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def send_poll(self, chat_id: str, question: str, options: List[str]) -> Message:
    """Sends poll through the Rubika API.

Args:
    chat_id: Identifier of the target chat.
    question: Value used by this operation.
    options: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
    '"""Rubika client operation ``send_poll``.\n\nArgs:\n    chat_id: Value accepted by this operation.\n    question: Value accepted by this operation.\n    options: Value accepted by this operation.\n\nReturns:\n    Message: The value returned by the Rubika API or the local helper.\n\nRaises:\n    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.\n"""'
    payload: Dict[str, object] = {'chat_id': chat_id, 'question': question, 'options': list(options)}
    data = await self._call('sendPoll', json_body=payload)
    return self._parse_message_id_response(data, 'sendPoll')
