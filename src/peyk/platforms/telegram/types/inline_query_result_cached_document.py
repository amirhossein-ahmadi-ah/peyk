from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultCachedDocument:
    """Represents a link to a file stored on the Telegram servers. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file.

Attributes:
    type: Type of the result, must be document
    id: Unique identifier for this result, 1-64 bytes
    title: Title for the result
    document_file_id: A valid file identifier for the file
    description: Short description of the result
    caption: Caption of the document to be sent, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the document caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the file"""
    id: str
    title: str
    document_file_id: str
    type: str = 'document'
    description: Optional[str] = None
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[Sequence[Union[MessageEntity, Mapping[str, object]]]] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None
    input_message_content: Optional[Union[InputMessageContent, Mapping[str, object]]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'title': self.title, 'document_file_id': self.document_file_id}
        if self.description is not None:
            body['description'] = self.description
        if self.caption is not None:
            body['caption'] = self.caption
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        entities = _serialize_entities(self.caption_entities)
        if entities is not None:
            body['caption_entities'] = entities
        _apply_result_markup(body, self)
        return body
