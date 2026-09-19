"""Declarative FSM states compatible with aiogram 3 semantics."""
from __future__ import annotations

import inspect
from collections.abc import Iterator
from typing import ClassVar


class State:
    """Describe one named FSM state, optionally with an explicit group name."""

    def __init__(self, state: str | None = None, group_name: str | None = None) -> None:
        self._state = state
        self._group_name = group_name
        self._group: type[StatesGroup] | None = None

    @property
    def group(self) -> type[StatesGroup]:
        """Return the owning state-group class."""
        if self._group is None:
            raise RuntimeError("This state is not in any group.")
        return self._group

    @property
    def state(self) -> str | None:
        """Return the fully-qualified state name."""
        if self._state is None or self._state == "*":
            return self._state
        if self._group_name is not None:
            group_name = self._group_name
        elif self._group is not None:
            group_name = self._group.__full_group_name__
        else:
            group_name = "@"
        return f"{group_name}:{self._state}"

    def set_parent(self, group: type[StatesGroup]) -> None:
        """Bind this state to a ``StatesGroup`` class."""
        if not issubclass(group, StatesGroup):
            raise ValueError("Group must be subclass of StatesGroup")
        self._group = group

    def __set_name__(self, owner: type[StatesGroup], name: str) -> None:
        if self._state is None:
            self._state = name
        self.set_parent(owner)

    def __str__(self) -> str:
        return f"<State '{self.state or ''}'>"

    __repr__ = __str__

    def __call__(self, event: object, raw_state: str | None = None) -> bool:
        """Match ``raw_state`` using the state's exact or wildcard value."""
        if self.state == "*":
            return True
        return raw_state == self.state

    def __eq__(self, other: object) -> bool:
        if isinstance(other, State):
            return self.state == other.state
        if isinstance(other, str):
            return self.state == other
        return NotImplemented

    def __hash__(self) -> int:
        return hash(self.state)


class StatesGroupMeta(type):
    """Collect direct and nested states when a state group is created."""

    __parent__: type[StatesGroup] | None
    __childs__: tuple[type[StatesGroup], ...]
    __states__: tuple[State, ...]
    __state_names__: tuple[str, ...]
    __all_childs__: tuple[type[StatesGroup], ...]
    __all_states__: tuple[State, ...]
    __all_states_names__: tuple[str, ...]

    def __new__(mcls, name: str, bases: tuple[type, ...], namespace: dict[str, object], **kwargs: object) -> StatesGroupMeta:
        cls = super().__new__(mcls, name, bases, namespace, **kwargs)
        states = tuple(value for value in namespace.values() if isinstance(value, State))
        children = tuple(
            value for value in namespace.values()
            if inspect.isclass(value) and isinstance(value, StatesGroupMeta)
        )
        cls.__parent__ = None
        cls.__childs__ = children
        cls.__states__ = states
        cls.__state_names__ = tuple(state.state for state in states if state.state is not None)
        for child in children:
            child.__parent__ = cls
            child._refresh_metadata()
        cls.__all_childs__ = cls._get_all_childs()
        cls.__all_states__ = cls._get_all_states()
        cls.__all_states_names__ = tuple(state.state for state in cls.__all_states__ if state.state)
        return cls

    @property
    def __full_group_name__(cls) -> str:
        if cls.__parent__ is not None:
            return f"{cls.__parent__.__full_group_name__}.{cls.__name__}"
        return cls.__name__

    def _refresh_metadata(cls) -> None:
        """Recalculate nested state names after a parent group is assigned."""
        cls.__state_names__ = tuple(state.state for state in cls.__states__ if state.state)
        for child in cls.__childs__:
            child._refresh_metadata()
        cls.__all_childs__ = cls._get_all_childs()
        cls.__all_states__ = cls._get_all_states()
        cls.__all_states_names__ = tuple(state.state for state in cls.__all_states__ if state.state)

    def _get_all_childs(cls) -> tuple[type[StatesGroup], ...]:
        result = cls.__childs__
        for child in cls.__childs__:
            result += child.__all_childs__
        return result

    def _get_all_states(cls) -> tuple[State, ...]:
        result = cls.__states__
        for child in cls.__childs__:
            result += child.__all_states__
        return result

    def __contains__(cls, item: object) -> bool:
        if isinstance(item, str):
            return item in cls.__all_states_names__
        if isinstance(item, State):
            return item in cls.__all_states__
        if isinstance(item, StatesGroupMeta):
            return item in cls.__all_childs__
        return False

    def __iter__(cls) -> Iterator[State]:
        return iter(cls.__all_states__)

    def __str__(cls) -> str:
        return f"<StatesGroup '{cls.__full_group_name__}'>"


class StatesGroup(metaclass=StatesGroupMeta):
    """Base class for declarative FSM state groups."""

    __parent__: ClassVar[type[StatesGroup] | None]
    __childs__: ClassVar[tuple[type[StatesGroup], ...]]
    __states__: ClassVar[tuple[State, ...]]
    __state_names__: ClassVar[tuple[str, ...]]
    __all_childs__: ClassVar[tuple[type[StatesGroup], ...]]
    __all_states__: ClassVar[tuple[State, ...]]
    __all_states_names__: ClassVar[tuple[str, ...]]

    @classmethod
    def get_root(cls) -> type[StatesGroup]:
        """Return the root group for a nested group."""
        if cls.__parent__ is None:
            return cls
        return cls.__parent__.get_root()

    def __call__(self, event: object, raw_state: str | None = None) -> bool:
        """Match when ``raw_state`` belongs to this group's states."""
        return raw_state in type(self).__all_states_names__

    def __str__(self) -> str:
        return f"StatesGroup {type(self).__full_group_name__}"


def _default_state() -> State:
    return State()


def _any_state() -> State:
    return State(state="*")


def _bind_special_state(state: State) -> State:
    return state


default_state = _bind_special_state(_default_state())
any_state = _bind_special_state(_any_state())

__all__ = ["State", "StatesGroup", "default_state", "any_state"]
