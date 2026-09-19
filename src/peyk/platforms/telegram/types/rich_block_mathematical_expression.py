from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence, Union

@dataclass
class RichBlockMathematicalExpression:
    """A block with a mathematical expression in LaTeX format, corresponding to the custom HTML tag .

Attributes:
    type: Type of the block, always 'mathematical_expression'
    expression: The mathematical expression in LaTeX format"""
    expression: str = ''

    @classmethod
    def from_dict(cls, data):
        """Provides the from dict operation for the Telegram integration.

Args:
    data: Value used by this operation."""
        'Executes the from_dict operation.\n        \n        Args:\n            data: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``Any``).\n        '
        return cls(expression=data.get('expression', '')) if data else None
