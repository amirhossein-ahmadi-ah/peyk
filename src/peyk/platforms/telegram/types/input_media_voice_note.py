from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputMediaVoiceNote:
    """Represents a voice message file to be sent.

Attributes:
    type: Type of the media, must be voice_note
    media: File to send. Pass a file_id to send a file that exists on the Telegram servers (recommended), pass an HTTP URL for Telegram to get a file from the Internet, or pass "attach://" to upload a new one using multipart/form-data under  name. More information on Sending Files
    caption: Caption of the voice message to be sent, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the voice message caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    duration: Duration of the voice message in seconds"""
    media: object
    type: str = 'voice_note'
    duration: Optional[int] = None
    waveform: Optional[str] = None

    def to_dict(self, media_ref: str) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Args:
    media_ref: Value used by this operation.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Args:\n            media_ref: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': 'voice_note', 'media': media_ref}
        if self.duration is not None:
            body['duration'] = self.duration
        if self.waveform is not None:
            body['waveform'] = self.waveform
        return body
