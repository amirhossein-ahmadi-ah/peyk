from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockTable:
    """A table, corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'table'
    cells: Cells of the table
    is_bordered: True, if the table has borders
    is_striped: True, if the table is striped
    caption: Caption of the table"""
    cells: Optional[List[object]] = None
    is_compact: Optional[bool] = None

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(cells=data.get('cells'), is_compact=data.get('is_compact')) if data else None
