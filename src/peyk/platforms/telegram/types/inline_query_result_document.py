from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultDocument:
    """Represents a link to a file. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file. Currently, only .PDF and .ZIP files can be sent using this method.

Attributes:
    type: Type of the result, must be document
    id: Unique identifier for this result, 1-64 bytes
    title: Title for the result
    document_url: A valid URL for the file
    mime_type: MIME type of the content of the file, either 'application/pdf' or 'application/zip'
    caption: Caption of the document to be sent, 0-1024 characters after entities parsing
    parse_mode: Mode for parsing entities in the document caption. See formatting options for more details.
    caption_entities: List of special entities that appear in the caption, which can be specified instead of parse_mode
    description: Short description of the result
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the file
    thumbnail_url: URL of the thumbnail (JPEG only) for the file
    thumbnail_width: Thumbnail width
    thumbnail_height: Thumbnail height"""
    id: str
    title: str
    document_url: str
    mime_type: str
    type: str = 'document'
    caption: Optional[str] = None
    parse_mode: Optional[str] = None
    caption_entities: Optional[Sequence[Union[MessageEntity, Mapping[str, object]]]] = None
    description: Optional[str] = None
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None
    input_message_content: Optional[Union[InputMessageContent, Mapping[str, object]]] = None
    thumbnail_url: Optional[str] = None
    thumbnail_width: Optional[int] = None
    thumbnail_height: Optional[int] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'title': self.title, 'document_url': self.document_url, 'mime_type': self.mime_type}
        if self.caption is not None:
            body['caption'] = self.caption
        if self.parse_mode is not None:
            body['parse_mode'] = self.parse_mode
        entities = _serialize_entities(self.caption_entities)
        if entities is not None:
            body['caption_entities'] = entities
        if self.description is not None:
            body['description'] = self.description
        _apply_result_markup(body, self)
        _apply_thumbnail_fields(body, self)
        return body
