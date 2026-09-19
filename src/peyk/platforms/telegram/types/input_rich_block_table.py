from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockTable:
    """A table, corresponding to the HTML tag .

Attributes:
    type: Type of the block, always 'table'
    cells: Cells of the table
    is_bordered: Pass True if the table has borders
    is_striped: Pass True if the table is striped
    caption: Caption of the table"""
    cells: Optional[List[object]] = None
    is_compact: Optional[bool] = None

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        body: Dict[str, object] = {'cells': self.cells or []}
        if self.is_compact is not None:
            body['is_compact'] = self.is_compact
        return body
