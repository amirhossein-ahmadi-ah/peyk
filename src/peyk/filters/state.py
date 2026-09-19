"""FSM state filter with aiogram-style dependency injection."""
from __future__ import annotations

import re
import warnings
from re import Pattern

from .base import BaseFilter
from peyk.fsm.state import State, StatesGroup, any_state, default_state
from peyk.fsm.context import FSMContext
from peyk.fsm.storage.base import BaseStorage

StateSpec = State | type[StatesGroup] | str | None | Pattern[str]


class StateFilter(BaseFilter):
    """Match ``raw_state`` injected by :class:`FSMContextMiddleware`.

    ``StateGroup`` values match any state in the group, ``re.Pattern`` values
    use ``match()``, ``None`` matches the default empty state, and
    :data:`peyk.fsm.state.any_state` matches every state.
    """

    def __init__(self, *states: StateSpec, storage: BaseStorage | None = None, platform: str | None = None) -> None:
        # Legacy Phase-4 form: StateFilter(state, storage).
        if states and not _is_state_spec(states[-1]) and storage is None and isinstance(states[-1], BaseStorage):
            storage = states[-1]
            states = states[:-1]
        if storage is not None:
            warnings.warn(
                "StateFilter(storage=...) is deprecated; FSMContextMiddleware injects raw_state automatically.",
                DeprecationWarning,
                stacklevel=2,
            )
        if not states:
            raise ValueError("StateFilter requires at least one state")
        self.states = states
        self.storage = storage
        self.platform = platform

    async def __call__(self, event: object, **data: object) -> bool:
        raw_state = data.get("raw_state")
        if self.storage is not None:
            warnings.warn(
                "StateFilter with explicit storage is deprecated; use Dispatcher FSM integration.",
                DeprecationWarning,
                stacklevel=2,
            )
            context = FSMContext(event, self.storage, platform=self.platform)
            raw_state = await context.get_state()
        if raw_state is not None and not isinstance(raw_state, str):
            return False
        return any(_matches(spec, raw_state) for spec in self.states)


def _is_state_spec(value: object) -> bool:
    return value is None or isinstance(value, (State, str, re.Pattern)) or (
        isinstance(value, type) and issubclass(value, StatesGroup)
    )


def _matches(spec: StateSpec, raw_state: str | None) -> bool:
    if spec is None or spec == default_state:
        return raw_state is None
    if spec == any_state or (isinstance(spec, State) and spec.state == "*"):
        return True
    if isinstance(spec, type) and issubclass(spec, StatesGroup):
        return raw_state in spec.__all_states_names__
    if isinstance(spec, State):
        return spec.state == raw_state
    if isinstance(spec, str):
        return spec == raw_state
    if isinstance(spec, re.Pattern):
        return spec.match(raw_state or "") is not None
    return False
