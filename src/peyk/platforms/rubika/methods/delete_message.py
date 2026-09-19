from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def delete_message(self, chat_id: str, message_id: str) -> bool:
    """Removes message through the Rubika API.

Args:
    chat_id: Identifier of the target chat.
    message_id: Identifier of the target message.

Returns:
    Result produced by the Rubika operation."""
    '"""Rubika client operation ``delete_message``.\n\nArgs:\n    chat_id: Value accepted by this operation.\n    message_id: Value accepted by this operation.\n\nReturns:\n    bool: The value returned by the Rubika API or the local helper.\n\nRaises:\n    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.\n"""'
    await self._call('deleteMessage', json_body={'chat_id': chat_id, 'message_id': message_id})
    return True
