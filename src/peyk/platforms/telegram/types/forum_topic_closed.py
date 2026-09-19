from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class ForumTopicClosed:
    """ForumTopicClosed Telegram Bot API type."""

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['ForumTopicClosed']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['ForumTopicClosed']``).\n        "
        return cls() if data is not None else None
