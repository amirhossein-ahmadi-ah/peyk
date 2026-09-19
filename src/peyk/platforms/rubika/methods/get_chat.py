from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def get_chat(self, chat_id: str) -> Chat:
    """Retrieves chat from the Rubika API.

Args:
    chat_id: Identifier of the target chat.

Returns:
    Result produced by the Rubika operation."""
    '"""Rubika client operation ``get_chat``.\n\nArgs:\n    chat_id: Value accepted by this operation.\n\nReturns:\n    Chat: The value returned by the Rubika API or the local helper.\n\nRaises:\n    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.\n"""'
    data = await self._call('getChat', json_body={'chat_id': chat_id})
    chat = Chat.from_dict(data)
    if chat is None:
        raise RubikaAPIError('getChat: empty data in OK response', error_code='INVALID_RESPONSE', error_message='<empty getChat data>', raw=data if isinstance(data, dict) else None)
    return chat
