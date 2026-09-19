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
def _keypad_to_dict(keypad: Union[Keypad, Dict[str, object], None]) -> Optional[Dict[str, object]]:
    '''"""Rubika client operation ``_keypad_to_dict``.

Args:
    keypad: Value accepted by this operation.

Returns:
    Optional[Dict[str, object]]: The value returned by the Rubika API or the local helper.

Raises:
    RubikaAPIError: If the Rubika API rejects the request or returns an invalid response.
"""'''
    if keypad is None:
        return None
    if isinstance(keypad, Keypad):
        return keypad.to_dict()
    return dict(keypad)
