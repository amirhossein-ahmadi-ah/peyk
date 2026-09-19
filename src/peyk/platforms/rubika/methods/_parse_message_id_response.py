from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple, Union

from peyk.transport import run_with_retry

from ..errors import RubikaAPIError, error_for_envelope
from ..models import (
    ChatTypeEnum,
    FileTypeEnum,
    ForwardedFromEnum,
    PollStatusEnum,
    ButtonSelectionTypeEnum,
    ButtonSelectionSearchEnum,
    ButtonSelectionGetEnum,
    ButtonCalendarTypeEnum,
    ButtonTextboxTypeKeypadEnum,
    ButtonTextboxTypeLineEnum,
    ButtonLocationTypeEnum,
    MessageSenderEnum,
    UpdateTypeEnum,
    ChatKeypadTypeEnum,
    UpdateEndpointTypeEnum,
    MetadataTypeEnum,
    EnumChatAccess,
    EventTypeEnum,
    EventJoinTypeEnum,
    ButtonTypeEnum,
    File,
    Location,
    Chat,
    Bot,
    BotCommand,
    Sticker,
    ContactMessage,
    PollStatus,
    Poll,
    ForwardedFrom,
    AuxData,
    MetadataPart,
    Metadata,
    ButtonSelectionItem,
    ButtonSelection,
    ButtonCalendar,
    ButtonNumberPicker,
    ButtonStringPicker,
    ButtonTextbox,
    ButtonLocation,
    Button,
    KeypadRow,
    Keypad,
    Message,
    Event,
    Update,
    InlineMessage,
    GetUpdatesResult,
)

@staticmethod
def _parse_message_id_response(data: object, method: str) -> Message:
    '''"""Rubika client operation ``_parse_message_id_response``.

Args:
    data: Value accepted by this operation.
    method: Value accepted by this operation.

Returns:
    Message: The value returned by the Rubika API or the local helper.

Raises:
    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.
"""'''
    if not isinstance(data, dict) or 'message_id' not in data:
        raise RubikaAPIError(f"{method}: response missing 'message_id'", error_code='INVALID_RESPONSE', error_message='<missing message_id>', raw=data if isinstance(data, dict) else None)
    return Message(message_id=str(data['message_id']))
