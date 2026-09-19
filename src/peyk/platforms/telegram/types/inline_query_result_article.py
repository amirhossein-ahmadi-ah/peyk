from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultArticle:
    """Represents a link to an article or web page.

Attributes:
    type: Type of the result, must be article
    id: Unique identifier for this result, 1-64 Bytes
    title: Title of the result
    input_message_content: Content of the message to be sent
    reply_markup: Inline keyboard attached to the message
    url: URL of the result
    description: Short description of the result
    thumbnail_url: Url of the thumbnail for the result
    thumbnail_width: Thumbnail width
    thumbnail_height: Thumbnail height
    hide_url: Pass True if you don't want the URL to be shown in the message"""
    id: str
    title: str
    input_message_content: Union[InputMessageContent, Mapping[str, object]]
    type: str = 'article'
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None
    url: Optional[str] = None
    description: Optional[str] = None
    thumbnail_url: Optional[str] = None
    thumbnail_width: Optional[int] = None
    thumbnail_height: Optional[int] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'title': self.title, 'input_message_content': _serialize_inline_content(self.input_message_content)}
        _apply_result_markup(body, self)
        if self.url is not None:
            body['url'] = self.url
        if self.description is not None:
            body['description'] = self.description
        _apply_thumbnail_fields(body, self)
        return body
