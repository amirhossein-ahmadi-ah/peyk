from __future__ import annotations
from dataclasses import dataclass, field
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class Contact:
    """This object represents a phone contact.

Attributes:
    phone_number: Contact's phone number
    first_name: Contact's first name
    last_name: Contact's last name
    user_id: Contact's user identifier in Telegram. This number may have more than 32 significant bits and some programming languages may have difficulty/silent defects in interpreting it. But it has at most 52 significant bits, so a 64-bit integer or double-precision float type are safe for storing this identifier.
    vcard: Additional data about the contact in the form of a vCard"""
    phone_number: str
    first_name: str
    last_name: Optional[str] = None
    user_id: Optional[int] = None
    vcard: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['Contact']:
        """Parse a Telegram API mapping into this type.

Args:
    data: Raw Telegram API mapping, or ``None``.

Returns:
    Parsed type instance, or ``None`` when ``data`` is ``None``."""
        if data is None:
            return None
        return cls(phone_number=data.get('phone_number', ''), first_name=data.get('first_name', ''), last_name=data.get('last_name'), user_id=data.get('user_id'), vcard=data.get('vcard'))
