from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def get_file(self, file_id: str) -> str:
    """Retrieves file from the Rubika API.

Args:
    file_id: Identifier of the file.

Returns:
    Result produced by the Rubika operation."""
    'Return the download URL for a file.\n    \n    Args:\n        file_id: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``str``).\n    '
    data = await self._call('getFile', json_body={'file_id': file_id})
    if isinstance(data, dict):
        return str(data.get('download_url', ''))
    return ''
