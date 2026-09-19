from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def request_send_file(self, type: str=FileTypeEnum.FILE) -> str:
    """Performs the request send file operation for the Rubika client.

Args:
    type: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
    'Request a temporary upload URL for a file type.\n    \n            Returns the ``upload_url`` to POST the actual file bytes to\n            (see ``upload_file`` below).\n            \n    \n    Args:\n        type: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``str``).\n    '
    data = await self._call('requestSendFile', json_body={'type': type})
    if isinstance(data, dict):
        return str(data.get('upload_url', ''))
    return ''
