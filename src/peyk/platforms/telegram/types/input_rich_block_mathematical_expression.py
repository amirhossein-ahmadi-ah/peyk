from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class InputRichBlockMathematicalExpression:
    """A block with a mathematical expression in LaTeX format, corresponding to the custom HTML tag .

Attributes:
    type: Type of the block, always 'mathematical_expression'
    expression: The mathematical expression in LaTeX format"""
    expression: str = ''

    def to_dict(self) -> Dict[str, object]:
        """Provides the to dict operation for the Telegram integration.

Returns:
    Result produced by the operation."""
        'Executes the to_dict operation.\n        \n        Returns:\n            The operation result (``Dict[str, object]``).\n        '
        return {'expression': self.expression}
