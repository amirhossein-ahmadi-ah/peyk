from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class PassportFile:
    """This object represents a file uploaded to Telegram Passport. Currently all Telegram Passport files are in JPEG format when decrypted and don't exceed 10MB.

Attributes:
    file_id: Identifier for this file, which can be used to download or reuse the file
    file_unique_id: Unique identifier for this file, which is supposed to be the same over time and for different bots. Can't be used to download or reuse the file.
    file_size: File size in bytes
    file_date: Unix time when the file was uploaded"""
    file_id: str
    file_unique_id: str
    file_size: int
    file_date: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['PassportFile']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['PassportFile']``).\n        "
        if data is None:
            return None
        return cls(file_id=_parse_api_value('String', data.get('file_id')), file_unique_id=_parse_api_value('String', data.get('file_unique_id')), file_size=_parse_api_value('Integer', data.get('file_size')), file_date=_parse_api_value('Integer', data.get('file_date')))
