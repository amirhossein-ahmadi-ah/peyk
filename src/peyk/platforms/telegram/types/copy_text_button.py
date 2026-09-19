from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class CopyTextButton:
    """This object represents an inline keyboard button that copies specified text to the clipboard.

Attributes:
    text: The text to be copied to the clipboard; 1-256 characters"""
    text: str = ''

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['CopyTextButton']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['CopyTextButton']``).\n        "
        if data is None:
            return None
        return cls(text=data.get('text', ''))

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'text': self.text}
