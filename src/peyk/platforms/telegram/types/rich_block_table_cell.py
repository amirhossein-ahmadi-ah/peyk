from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockTableCell:
    """Cell in a table.

Attributes:
    align: Horizontal cell content alignment. Currently, must be one of 'left', 'center', or 'right'.
    valign: Vertical cell content alignment. Currently, must be one of 'top', 'middle', or 'bottom'.
    text: Text in the cell. If omitted, then the cell is invisible.
    is_header: True, if the cell is a header cell
    colspan: The number of columns the cell spans if it is bigger than 1
    rowspan: The number of rows the cell spans if it is bigger than 1"""
    text: str = ''

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(text=data.get('text', '')) if data else None
