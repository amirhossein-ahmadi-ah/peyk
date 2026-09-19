from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class BusinessOpeningHours:
    """Describes the opening hours of a business.

Attributes:
    time_zone_name: Unique name of the time zone for which the opening hours are defined
    opening_hours: List of time intervals describing business opening hours"""
    time_zone_name: str
    opening_hours: List[BusinessOpeningHoursInterval]

    @classmethod
    def from_dict(cls, data: Optional[dict]) -> Optional['BusinessOpeningHours']:
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation.

Returns:
    Result produced by the operation."""
        "Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Optional['BusinessOpeningHours']``).\n        "
        if data is None:
            return None
        return cls(time_zone_name=_parse_api_value('String', data.get('time_zone_name')), opening_hours=_parse_api_value('Array of BusinessOpeningHoursInterval', data.get('opening_hours')))
