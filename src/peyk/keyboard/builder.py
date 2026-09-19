from __future__ import annotations
from copy import deepcopy
from typing import Generic, Iterator, TypeVar
from .ir import InlineButton, InlineKeyboard, ReplyButton, ReplyKeyboard
MAX_WIDTH = 8
MAX_BUTTONS = 100
B = TypeVar('B', InlineButton, ReplyButton)

class _Builder(Generic[B]):

    def __init__(self) -> None:
        self._markup: list[list[B]] = []

    @property
    def buttons(self) -> Iterator[B]:
        """Performs the buttons operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        return iter((b for row in self._markup for b in row))

    def _count(self) -> int:
        return sum((len(r) for r in self._markup))

    def _validate_count(self, n: int) -> None:
        if self._count() + n > MAX_BUTTONS:
            raise ValueError('too many buttons (maximum is 100)')

    def add(self, *buttons: B) -> '_Builder[B]':
        """Performs the add operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        self._validate_count(len(buttons))
        if not buttons:
            return self
        if not self._markup:
            self._markup.append([])
        for button in buttons:
            if len(self._markup[-1]) >= MAX_WIDTH:
                self._markup.append([])
            self._markup[-1].append(button)
        return self

    def row(self, *buttons: B, width: int=MAX_WIDTH) -> '_Builder[B]':
        """Performs the row operation for the keyboard client.

Args:
    width: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
        if not 1 <= width <= MAX_WIDTH:
            raise ValueError('width must be between 1 and 8')
        self._validate_count(len(buttons))
        if not buttons:
            return self
        self._markup.extend([list(buttons[i:i + width]) for i in range(0, len(buttons), width)])
        return self

    def adjust(self, *sizes: int, repeat: bool=False) -> '_Builder[B]':
        """Performs the adjust operation for the keyboard client.

Args:
    repeat: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
        if not sizes or any((s < 1 or s > MAX_WIDTH for s in sizes)):
            raise ValueError('row sizes must be between 1 and 8')
        items = list(self.buttons)
        self._markup = []
        i = 0
        si = 0
        while i < len(items):
            size = sizes[si % len(sizes)] if repeat else sizes[min(si, len(sizes) - 1)]
            self._markup.append(items[i:i + size])
            i += size
            si += 1
        return self

    def attach(self, other: '_Builder[B]') -> '_Builder[B]':
        """Performs the attach operation for the keyboard client.

Args:
    other: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
        self._validate_count(other._count())
        self._markup.extend(deepcopy(other._markup))
        return self

    def copy(self) -> '_Builder[B]':
        """Performs the copy operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        return deepcopy(self)

    def export(self) -> list[list[B]]:
        """Performs the export operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        return deepcopy(self._markup)

class InlineKeyboardBuilder(_Builder[InlineButton]):
    """Build an inline keyboard without selecting a platform."""

    def button(self, **fields: object) -> 'InlineKeyboardBuilder':
        """Performs the button operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        return self.add(InlineButton(**fields))

    def as_markup(self, **options: object) -> InlineKeyboard:
        """Performs the as markup operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        return InlineKeyboard(tuple((tuple(r) for r in self.export())))

    @classmethod
    def from_markup(cls, markup: InlineKeyboard) -> 'InlineKeyboardBuilder':
        """Performs the from markup operation for the keyboard client.

Args:
    markup: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
        b = cls()
        b._markup = [list(r) for r in markup.inline_keyboard]
        return b

class ReplyKeyboardBuilder(_Builder[ReplyButton]):
    """Build a reply keyboard without selecting a platform."""

    def button(self, **fields: object) -> 'ReplyKeyboardBuilder':
        """Performs the button operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        return self.add(ReplyButton(**fields))

    def as_markup(self, **options: object) -> ReplyKeyboard:
        """Performs the as markup operation for the keyboard client.

Returns:
    Result produced by the keyboard operation."""
        allowed = {'resize_keyboard', 'one_time_keyboard', 'input_field_placeholder', 'is_persistent', 'selective'}
        return ReplyKeyboard(tuple((tuple(r) for r in self.export())), **{k: v for k, v in options.items() if k in allowed})

    @classmethod
    def from_markup(cls, markup: ReplyKeyboard) -> 'ReplyKeyboardBuilder':
        """Performs the from markup operation for the keyboard client.

Args:
    markup: Value used by this operation.

Returns:
    Result produced by the keyboard operation."""
        b = cls()
        b._markup = [list(r) for r in markup.keyboard]
        return b
