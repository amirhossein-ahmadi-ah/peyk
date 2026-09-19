from __future__ import annotations
from dataclasses import dataclass

class SkipHandler(Exception):
    """Signal that the current handler did not handle the event."""

class _Unhandled:
    def __repr__(self) -> str: return "UNHANDLED"
UNHANDLED = _Unhandled()

@dataclass(frozen=True)
class ErrorEvent:
    """An exception raised while processing a normalized event."""
    event: object
    exception: Exception
