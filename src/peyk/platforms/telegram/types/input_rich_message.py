from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichMessage:
    """Describes a rich message to be sent. Exactly one of the fields html, markdown, or blocks must be used.

Attributes:
    html: Content of the rich message to send described using HTML formatting. See rich message formatting options for more details. Use media field to specify the media used in the message.
    markdown: Content of the rich message to send described using Markdown formatting. See rich message formatting options for more details. Use media field to specify the media used in the message.
    is_rtl: Pass True if the rich message must be shown right-to-left
    skip_entity_detection: Pass True to skip automatic detection of entities (e.g., URLs, email addresses, username mentions, hashtags, cashtags, bot commands, or phone numbers) in the text
    blocks: Content of the rich message to send described as a list of blocks
    media: List of media that are specified in the markdown or html fields using tg://photo?id=, tg://video?id=, and tg://audio?id= links"""
    text: Optional[str] = None
    parse_mode: Optional[str] = None
    blocks: Optional[object] = None
    media: Optional[object] = None
    is_rtl: Optional[bool] = None
    skip_entity_detection: Optional[bool] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {}
        for key in ('text', 'parse_mode', 'blocks', 'media', 'is_rtl', 'skip_entity_detection'):
            value = getattr(self, key)
            if value is not None:
                body[key] = _serialize_api_value(value)
        return body

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['InputRichMessage']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['InputRichMessage']``).\n        "
        if data is None:
            return None
        return cls(**{k: data.get(k) for k in ('text', 'parse_mode', 'blocks', 'media', 'is_rtl', 'skip_entity_detection')})
