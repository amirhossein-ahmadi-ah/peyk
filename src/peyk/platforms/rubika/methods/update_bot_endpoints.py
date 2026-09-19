from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union
from peyk.transport import run_with_retry
from ..errors import RubikaAPIError, error_for_envelope
from ..models import ChatTypeEnum, FileTypeEnum, ForwardedFromEnum, PollStatusEnum, ButtonSelectionTypeEnum, ButtonSelectionSearchEnum, ButtonSelectionGetEnum, ButtonCalendarTypeEnum, ButtonTextboxTypeKeypadEnum, ButtonTextboxTypeLineEnum, ButtonLocationTypeEnum, MessageSenderEnum, UpdateTypeEnum, ChatKeypadTypeEnum, UpdateEndpointTypeEnum, MetadataTypeEnum, EnumChatAccess, EventTypeEnum, EventJoinTypeEnum, ButtonTypeEnum, File, Location, Chat, Bot, BotCommand, Sticker, ContactMessage, PollStatus, Poll, ForwardedFrom, AuxData, MetadataPart, Metadata, ButtonSelectionItem, ButtonSelection, ButtonCalendar, ButtonNumberPicker, ButtonStringPicker, ButtonTextbox, ButtonLocation, Button, KeypadRow, Keypad, Message, Event, Update, InlineMessage, GetUpdatesResult

async def update_bot_endpoints(self, url: str, type: str=UpdateEndpointTypeEnum.RECEIVE_UPDATE) -> bool:
    """Performs the update bot endpoints operation for the Rubika client.

Args:
    url: Target URL.
    type: Value used by this operation.

Returns:
    Result produced by the Rubika operation."""
    'Register an endpoint URL for a given event type.\n    \n            ``type`` is one of ``UpdateEndpointTypeEnum``: ReceiveUpdate,\n            ReceiveInlineMessage, ReceiveQuery, GetSelectionItem,\n            SearchSelectionItems.\n            \n    \n    Args:\n        url: Value of the declared parameter type.\n        type: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``bool``).\n    '
    await self._call('updateBotEndpoints', json_body={'url': url, 'type': type})
    return True
