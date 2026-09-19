from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PassportData:
    """Describes Telegram Passport data shared with the bot by the user.

Attributes:
    data: Array with information about documents and other Telegram Passport elements that was shared with the bot
    credentials: Encrypted credentials required to decrypt the data"""
    data: List[EncryptedPassportElement]
    credentials: EncryptedCredentials

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PassportData']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PassportData']``).\n        "
        if data is None:
            return None
        return cls(data=_parse_api_value('Array of EncryptedPassportElement', data.get('data')), credentials=_parse_api_value('EncryptedCredentials', data.get('credentials')))
