from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable
from peyk.filters import BaseFilter

@dataclass(frozen=True)
class HandlerObject:
    """HandlerObject provides the dispatcher API surface used by peyk."""
    callback: Callable[..., object]
    filters: tuple[BaseFilter, ...] = field(default_factory=tuple)
