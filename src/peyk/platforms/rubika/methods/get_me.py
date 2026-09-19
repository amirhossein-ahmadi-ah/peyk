from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def get_me(self) -> Bot:
    """Retrieves me from the Rubika API.

Returns:
    Result produced by the Rubika operation."""
    '"""Rubika client operation ``get_me``.\n\nArgs:\n    None.\n\nReturns:\n    Bot: The value returned by the Rubika API or the local helper.\n\nRaises:\n    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.\n"""'
    data = await self._call('getMe')
    bot = Bot.from_dict(data)
    if bot is None:
        raise RubikaAPIError('getMe: empty data in OK response', error_code='INVALID_RESPONSE', error_message='<empty getMe data>', raw=data if isinstance(data, dict) else None)
    return bot
