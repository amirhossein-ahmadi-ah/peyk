from __future__ import annotations
import inspect
from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import TypeVar
EventT = TypeVar('EventT')
FilterResult = bool | dict[str, object]

class BaseFilter(ABC):
    """Base class for filters that may also contribute handler data."""

    @abstractmethod
    async def __call__(self, event: EventT, **data: object) -> FilterResult:
        """Evaluate the filter and optionally return values for dependency injection."""
        raise NotImplementedError

    def __and__(self, other: object) -> BaseFilter:
        return and_f(self, other)

    def __or__(self, other: object) -> BaseFilter:
        return or_f(self, other)

    def __invert__(self) -> BaseFilter:
        return invert_f(self)

class CallableFilter(BaseFilter):
    """Adapt a synchronous or asynchronous callable to ``BaseFilter``."""

    def __init__(self, callback: Callable[..., object]) -> None:
        if not callable(callback):
            raise TypeError('filter must be callable')
        self.callback = callback
        try:
            self._accepts_data = any((p.kind is inspect.Parameter.VAR_KEYWORD for p in inspect.signature(callback).parameters.values())) or len(inspect.signature(callback).parameters) >= 2
        except (TypeError, ValueError):
            self._accepts_data = True

    async def __call__(self, event: object, **data: object) -> FilterResult:
        if self._accepts_data:
            result = self.callback(event, **data)
        else:
            result = self.callback(event)
        if inspect.isawaitable(result):
            result = await result
        if isinstance(result, dict):
            return {str(k): v for k, v in result.items()}
        return bool(result)

def normalize_filter(value: object) -> BaseFilter:
    """Provides the normalize filter operation for the peyk integration.

Args:
    value: Value used by this operation.

Returns:
    Result produced by the operation."""
    if isinstance(value, BaseFilter):
        return value
    return CallableFilter(value)

class _AndFilter(BaseFilter):

    def __init__(self, filters: tuple[BaseFilter, ...]) -> None:
        self.filters = filters

    async def __call__(self, event: object, **data: object) -> FilterResult:
        merged: dict[str, object] = {}
        for filter_ in self.filters:
            context = dict(data)
            context.update(merged)
            result = await filter_(event, **context)
            if not result:
                return False
            if isinstance(result, dict):
                merged.update(result)
        return merged or True

class _OrFilter(BaseFilter):

    def __init__(self, filters: tuple[BaseFilter, ...]) -> None:
        self.filters = filters

    async def __call__(self, event: object, **data: object) -> FilterResult:
        for filter_ in self.filters:
            result = await filter_(event, **data)
            if result:
                return result
        return False

class _InvertFilter(BaseFilter):

    def __init__(self, filter_: BaseFilter) -> None:
        self.filter = filter_

    async def __call__(self, event: object, **data: object) -> FilterResult:
        return not bool(await self.filter(event, **data))

def and_f(*filters: object) -> BaseFilter:
    """Provides the and f operation for the peyk integration.

Returns:
    Result produced by the operation."""
    return _AndFilter(tuple((normalize_filter(f) for f in filters)))

def or_f(*filters: object) -> BaseFilter:
    """Provides the or f operation for the peyk integration.

Returns:
    Result produced by the operation."""
    return _OrFilter(tuple((normalize_filter(f) for f in filters)))

def invert_f(filter_: object) -> BaseFilter:
    """Provides the invert f operation for the peyk integration.

Args:
    filter_: Value used by this operation.

Returns:
    Result produced by the operation."""
    return _InvertFilter(normalize_filter(filter_))
