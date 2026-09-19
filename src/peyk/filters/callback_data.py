from __future__ import annotations
import types
import uuid
from dataclasses import fields, is_dataclass, dataclass
from decimal import Decimal
from enum import Enum
from typing import ClassVar, Union, Mapping, TypeVar, get_args, get_origin, get_type_hints
from abc import ABCMeta
from .base import BaseFilter

class CallbackDataMeta(ABCMeta):
    """CallbackDataMeta defines a public API type for peyk."""

    def __new__(mcls, name: str, bases: tuple[type, ...], namespace: Mapping[str, object], **kwargs: object) -> type:
        prefix = kwargs.pop('prefix', None)
        sep = kwargs.pop('sep', ':')
        cls = super().__new__(mcls, name, bases, namespace)
        if prefix is not None:
            if not isinstance(prefix, str) or not prefix or sep in prefix:
                raise ValueError('invalid CallbackData prefix')
            cls.__callback_prefix__ = prefix
            cls.__callback_sep__ = str(sep)
            cls = dataclass(cls)
        return cls
CallbackDataT = TypeVar('CallbackDataT', bound='CallbackData')

class CallbackData(BaseFilter, metaclass=CallbackDataMeta):
    """Dataclass-based callback-data factory compatible with aiogram's model."""
    __callback_prefix__: ClassVar[str]
    __callback_sep__: ClassVar[str] = ':'

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)

    def pack(self) -> str:
        """Provides the pack operation for the peyk integration.

Returns:
    Result produced by the operation."""
        prefix, sep = (self.__callback_prefix__, self.__callback_sep__)
        values = [prefix]
        hints = get_type_hints(type(self))
        for field in fields(self):
            value = getattr(self, field.name)
            encoded = _encode(value, hints[field.name])
            if sep in encoded:
                raise ValueError(f'separator {sep!r} appears in {field.name}')
            values.append(encoded)
        return sep.join(values)

    @classmethod
    def unpack(cls: type[CallbackDataT], value: str) -> CallbackDataT:
        """Provides the unpack operation for the peyk integration.

Args:
    value: Value used by this operation.

Returns:
    Result produced by the operation."""
        sep = cls.__callback_sep__
        parts = value.split(sep)
        if not parts or parts[0] != cls.__callback_prefix__:
            raise ValueError('invalid callback-data prefix')
        hints = get_type_hints(cls)
        names = [f.name for f in fields(cls)]
        if len(parts) != len(names) + 1:
            raise ValueError('invalid callback-data field count')
        return cls(**{n: _decode(v, hints[n]) for n, v in zip(names, parts[1:])})

    @classmethod
    def filter(cls, magic: object | None=None) -> BaseFilter:
        """Provides the filter operation for the peyk integration.

Args:
    magic: Value used by this operation.

Returns:
    Result produced by the operation."""
        return _CallbackDataFilter(cls, magic)

    async def __call__(self, event: object, **data: object) -> bool:
        return False

class _CallbackDataFilter(BaseFilter):

    def __init__(self, cls: type[CallbackData], magic: object | None) -> None:
        self.cls, self.magic = (cls, magic)

    async def __call__(self, event: object, **data: object) -> bool | dict[str, object]:
        raw = getattr(event, 'data', None)
        if not isinstance(raw, str):
            return False
        try:
            obj = self.cls.unpack(raw)
        except (TypeError, ValueError):
            return False
        if self.magic is not None:
            from .base import normalize_filter
            if not await normalize_filter(self.magic)(obj, **data):
                return False
        return {'callback_data': obj}

def _encode(value: object, annotation: object) -> str:
    if value is None:
        return ''
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, bool):
        return '1' if value else '0'
    if isinstance(value, (str, int, float, (UUID := uuid.UUID), Decimal)):
        return str(value)
    raise TypeError(f'unsupported CallbackData field type: {type(value).__name__}')

def _decode(value: str, annotation: object) -> object:
    origin = get_origin(annotation)
    args = get_args(annotation)
    if origin in (Union, types.UnionType):
        non_none = [a for a in args if a is not type(None)]
        if value == '' and len(non_none) < len(args):
            return None
        return _decode(value, non_none[0])
    if annotation is str:
        return value
    if annotation is int:
        return int(value)
    if annotation is float:
        return float(value)
    if annotation is bool:
        if value not in {'0', '1', 'false', 'true'}:
            raise ValueError('invalid bool')
        return value in {'1', 'true'}
    if annotation is uuid.UUID:
        return uuid.UUID(value)
    if annotation is Decimal:
        return Decimal(value)
    if isinstance(annotation, type) and issubclass(annotation, Enum):
        return annotation(value)
    raise TypeError(f'unsupported CallbackData field type: {annotation!r}')

class CallbackDataEquals(BaseFilter):
    """Match an exact callback-data string."""

    def __init__(self, value: str) -> None:
        self.value = value

    async def __call__(self, event: object, **data: object) -> bool:
        return getattr(event, 'data', None) == self.value

class CallbackDataStartsWith(BaseFilter):
    """Match callback data beginning with a prefix."""

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    async def __call__(self, event: object, **data: object) -> bool:
        value = getattr(event, 'data', None)
        return isinstance(value, str) and value.startswith(self.prefix)
