from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union
from .input_media_link import InputMediaLink
from .input_media_location import InputMediaLocation
from .input_media_venue import InputMediaVenue
from .message_entity import MessageEntity

@dataclass
class InputPollOption:
    """This object contains information about one answer option in a poll to be sent.

Attributes:
    text: Option text, 1-100 characters
    text_parse_mode: Mode for parsing entities in the text. See formatting options for more details. Currently, only custom emoji entities are allowed.
    text_entities: A JSON-serialized list of special entities that appear in the poll option text. It can be specified instead of text_parse_mode.
    media: Media added to the poll option"""
    text: str
    text_parse_mode: Optional[str] = None
    text_entities: Optional[List[MessageEntity]] = None
    media: Optional[InputPollOptionMedia] = None

    def to_dict(self) -> Dict[str, object]:
        """Serialize this type to the Telegram API request shape.
        
        Returns:
            A JSON-compatible mapping representing this value.
        
        Raises:
            ValueError: Raised when the operation cannot complete.
        """
        body: Dict[str, object] = {'text': self.text}
        if self.text_parse_mode is not None:
            body['text_parse_mode'] = self.text_parse_mode
        if self.text_entities is not None:
            body['text_entities'] = [e.to_dict() for e in self.text_entities]
        if self.media is not None:
            media = self.media
            if isinstance(media, (InputMediaLocation, InputMediaVenue, InputMediaLink)):
                body['media'] = media.to_dict()
            elif isinstance(media.media, str):
                body['media'] = media.to_dict(media.media)
            else:
                raise ValueError(f'InputPollOption media must be a file_id/URL string (got upload content in {type(media).__name__}); sendPoll has no multipart upload path')
        return body
