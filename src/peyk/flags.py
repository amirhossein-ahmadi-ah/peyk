from __future__ import annotations
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import TypeVar
T = TypeVar('T', bound=Callable[..., object])

@dataclass(frozen=True)
class FlagDecorator:
    """FlagDecorator defines a public API type for peyk."""
    name: str
    value: object

    def __call__(self, handler: T) -> T:
        flags = dict(getattr(handler, '__peyk_flags__', {}))
        flags[self.name] = self.value
        setattr(handler, '__peyk_flags__', flags)
        return handler

class Flags:
    """Factory for handler flags used by dispatcher middleware."""

    def __getattr__(self, name: str) -> Callable[[object], FlagDecorator]:

        def decorator(value: object=True) -> FlagDecorator:
            return FlagDecorator(name, value)
        return decorator

def _flags_from(handler: object) -> dict[str, object]:
    return dict(getattr(handler, '__peyk_flags__', {}))

def get_flag(handler: object, name: str, default: object=None) -> object:
    """Return one registered handler flag."""
    return _flags_from(handler).get(name, default)

def check_flags(flags: Mapping[str, object], required: Mapping[str, object] | None=None) -> bool:
    """Check that every requested flag exists and matches its required value."""
    if required is None:
        return True
    return all((flags.get(name) == value for name, value in required.items()))
flags = Flags()
__all__ = ['FlagDecorator', 'Flags', 'check_flags', 'flags', 'get_flag']
