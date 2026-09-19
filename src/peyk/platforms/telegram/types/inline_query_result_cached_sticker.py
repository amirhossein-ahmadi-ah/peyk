from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultCachedSticker:
    """Represents a link to a sticker stored on the Telegram servers. By default, this sticker will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the sticker.

Attributes:
    type: Type of the result, must be sticker
    id: Unique identifier for this result, 1-64 bytes
    sticker_file_id: A valid file identifier of the sticker
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the sticker"""
    id: str
    sticker_file_id: str
    type: str = 'sticker'
    reply_markup: Optional[Union[InlineKeyboardMarkup, Mapping[str, object]]] = None
    input_message_content: Optional[Union[InputMessageContent, Mapping[str, object]]] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'sticker_file_id': self.sticker_file_id}
        _apply_result_markup(body, self)
        return body
