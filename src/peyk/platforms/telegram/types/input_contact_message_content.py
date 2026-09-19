from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputContactMessageContent:
    """Represents the content of a contact message to be sent as the result of an inline query.

Attributes:
    phone_number: Contact's phone number
    first_name: Contact's first name
    last_name: Contact's last name
    vcard: Additional data about the contact in the form of a vCard, 0-2048 bytes"""
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    vcard: Optional[str] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'phone_number': self.phone_number, 'first_name': self.first_name}
        if self.last_name is not None:
            body['last_name'] = self.last_name
        if self.vcard is not None:
            body['vcard'] = self.vcard
        return body
