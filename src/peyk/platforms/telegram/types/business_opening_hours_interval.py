from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BusinessOpeningHoursInterval:
    """Describes an interval of time during which a business is open.

Attributes:
    opening_minute: The minute's sequence number in a week, starting on Monday, marking the start of the time interval during which the business is open; 0 - 7  24  60
    closing_minute: The minute's sequence number in a week, starting on Monday, marking the end of the time interval during which the business is open; 0 - 8  24  60"""
    opening_minute: int
    closing_minute: int

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BusinessOpeningHoursInterval']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BusinessOpeningHoursInterval']``).\n        "
        if data is None:
            return None
        return cls(opening_minute=_parse_api_value('Integer', data.get('opening_minute')), closing_minute=_parse_api_value('Integer', data.get('closing_minute')))
