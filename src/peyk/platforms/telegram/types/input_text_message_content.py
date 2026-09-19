from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputTextMessageContent:
    """Represents the content of a text message to be sent as the result of an inline query.

Attributes:
    message_text: Text of the message to be sent, 1-4096 characters
    parse_mode: Mode for parsing entities in the message text. See formatting options for more details.
    entities: List of special entities that appear in message text, which can be specified instead of parse_mode
    link_preview_options: Link preview generation options for the message
    disable_web_page_preview: Disables link previews for links in the sent message"""
    message_text: str
    parse_mode: Optional[str] = None
    entities: Optional[Sequence[Union[MessageEntity, Mapping[str, object]]]] = None
    link_preview_options: Optional[Union[LinkPreviewOptions, Mapping[str, object]]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'message_text': self.message_text}
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        entities = _serialize_entities(self.entities)
        if entities is not None:
            body['entities'] = entities
        if self.link_preview_options is not None:
            if isinstance(self.link_preview_options, LinkPreviewOptions):
                body['link_preview_options'] = self.link_preview_options.to_dict()
            else:
                body['link_preview_options'] = dict(self.link_preview_options)
        return body
