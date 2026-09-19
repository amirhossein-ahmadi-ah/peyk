from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class EncryptedCredentials:
    """Describes data required for decrypting and authenticating EncryptedPassportElement. See the Telegram Passport Documentation for a complete description of the data decryption and authentication processes.

Attributes:
    data: Base64-encoded encrypted JSON-serialized data with unique user's payload, data hashes and secrets required for EncryptedPassportElement decryption and authentication
    hash: Base64-encoded data hash for data authentication
    secret: Base64-encoded secret, encrypted with the bot's public RSA key, required for data decryption"""
    data: str
    hash: str
    secret: str

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['EncryptedCredentials']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['EncryptedCredentials']``).\n        "
        if data is None:
            return None
        return cls(data=_parse_api_value('String', data.get('data')), hash=_parse_api_value('String', data.get('hash')), secret=_parse_api_value('String', data.get('secret')))
