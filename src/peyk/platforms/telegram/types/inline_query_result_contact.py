from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InlineQueryResultContact:
    """Represents a contact with a phone number. By default, this contact will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the contact.

Attributes:
    type: Type of the result, must be contact
    id: Unique identifier for this result, 1-64 Bytes
    phone_number: Contact's phone number
    first_name: Contact's first name
    last_name: Contact's last name
    vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes
    reply_markup: Inline keyboard attached to the message
    input_message_content: Content of the message to be sent instead of the contact
    thumbnail_url: Url of the thumbnail for the result
    thumbnail_width: Thumbnail width
    thumbnail_height: Thumbnail height"""
    id: str
    phone_number: str
    first_name: str
    type: str = 'contact'
    last_name: Optional[str] = None
    vcard: Optional[str] = None
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
        body: Dict[str, object] = {'type': self.type, 'id': self.id, 'phone_number': self.phone_number, 'first_name': self.first_name}
        if self.last_name is not None:
            body['last_name'] = self.last_name
        if self.vcard is not None:
            body['vcard'] = self.vcard
        _apply_result_markup(body, self)
        _apply_thumbnail_fields(body, self)
        return body
