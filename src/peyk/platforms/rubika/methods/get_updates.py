from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def get_updates(self, *, offset_id: Optional[str]=None, limit: Optional[int]=None) -> Tuple[List[Update], Optional[str]]:
    """Retrieves updates from the Rubika API.

Args:
    offset_id: Value used by this operation.
    limit: Maximum number of results requested.

Returns:
    Result produced by the Rubika operation."""
    'Long-poll for updates.\n    \n            Returns ``(updates, next_offset_id)``. Pass the returned\n            ``next_offset_id`` as ``offset_id`` on the next call.\n            \n    \n    Args:\n        offset_id: Value of the declared parameter type.\n        limit: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``Tuple[List[Update], Optional[str]]``).\n    '
    payload: Dict[str, object] = {}
    if offset_id is not None:
        payload['offset_id'] = offset_id
    if limit is not None:
        payload['limit'] = limit
    data = await self._call('getUpdates', json_body=payload)
    result = GetUpdatesResult.from_data(data)
    return (result.updates, result.next_offset_id)
