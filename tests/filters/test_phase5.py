from __future__ import annotations
from decimal import Decimal
from enum import Enum
from uuid import UUID

import pytest

from peyk import F
from peyk.dispatcher import ErrorEvent, Router, SkipHandler, UNHANDLED
from peyk.filters import (
    CallbackData, ChatTypeFilter, Command, CommandStart, ExceptionTypeFilter,
    MagicData, PlatformFilter, SupportsFilter, TextEquals, and_f, invert_f, or_f,
)
from peyk.platform_core.capabilities import Feature
from peyk.types import Chat, ChatType, ContentType, Message, User


class FakeBot:
    def __init__(self, platform: str = "telegram") -> None:
        self.platform = platform
    async def me(self):
        return User(99, True, "Bot", username="my_bot")
    def supports(self, feature: Feature) -> bool:
        return feature is Feature.TEXT


def event(text: str = "hi", platform: str = "telegram") -> Message:
    return Message(
        text=text,
        from_user=User(1, False, "Alice"),
        chat=Chat(10, ChatType.PRIVATE),
        content_type=ContentType.TEXT,
        bot=FakeBot(platform),
    )


@pytest.mark.asyncio
async def test_first_match_and_skip_handler() -> None:
    router = Router()
    seen: list[str] = []

    @router.message()
    async def first(message: Message) -> None:
        seen.append("first")
        raise SkipHandler

    @router.message()
    async def second(message: Message) -> str:
        seen.append("second")
        return "handled"

    assert await router.propagate_event(event()) == "handled"
    assert seen == ["first", "second"]


@pytest.mark.asyncio
async def test_nested_router_order_is_depth_first_inclusion_order() -> None:
    root = Router()
    left = Router()
    right = Router()
    root.include_router(left).include_router(right)
    seen: list[str] = []

    @left.message()
    async def left_handler(message: Message) -> None:
        seen.append("left")

    @right.message()
    async def right_handler(message: Message) -> None:
        seen.append("right")

    assert await root.propagate_event(event()) is None
    assert seen == ["left"]


@pytest.mark.asyncio
async def test_observer_filter_and_dict_result_inject_handler_data() -> None:
    router = Router()
    router.message.filter(F.text == "hello")
    received: list[int] = []

    class AddOne(TextEquals):
        async def __call__(self, event: object, **data: object) -> dict[str, object]:
            return {"number": 42}

    @router.message.register
    async def handler(message: Message, number: int) -> None:
        received.append(number)

    # Replace the registered callback's filter surface explicitly.
    router.message.handlers[-1] = type(router.message.handlers[-1])(handler, (AddOne("hello"),))
    await router.propagate_event(event("hello"))
    assert received == [42]


@pytest.mark.asyncio
async def test_error_observer_receives_error_event_and_stops_current_candidate() -> None:
    router = Router()
    errors: list[str] = []

    @router.errors(ExceptionTypeFilter(ValueError))
    async def on_error(error: ErrorEvent) -> None:
        errors.append(str(error.exception))

    @router.message()
    async def bad(message: Message) -> None:
        raise ValueError("boom")

    assert await router.propagate_event(event()) is UNHANDLED
    assert errors == ["boom"]


@pytest.mark.asyncio
async def test_observer_inner_and_outer_middleware_order() -> None:
    router = Router()
    trace: list[str] = []

    class Middleware:
        def __init__(self, name: str) -> None: self.name = name
        async def __call__(self, handler, event, data):
            trace.append(self.name + ":before")
            try: return await handler()
            finally: trace.append(self.name + ":after")

    router.message.outer_middleware(Middleware("outer"))
    router.message.middleware(Middleware("inner"))

    @router.message()
    async def handler(message: Message) -> None:
        trace.append("handler")

    await router.propagate_event(event())
    assert trace == ["outer:before", "inner:before", "handler", "inner:after", "outer:after"]


@pytest.mark.asyncio
async def test_magic_filter_expression_works_on_neutral_objects_for_all_platforms() -> None:
    for platform in ("telegram", "bale", "rubika"):
        current = event("hi", platform)
        assert (F.text == "hi")(current)
        assert (F.from_user.id == 1)(current)
        assert (F.chat.type == ChatType.PRIVATE)(current)
        assert (F.content_type == ContentType.TEXT)(current)
        assert F.text.startswith("h")(current)
        assert F.text.regexp(r"h.")(current)
        assert F.text.lower().in_({"hi"})(event("HI", platform))
        assert (F.bot.platform == platform)(current)


@pytest.mark.asyncio
async def test_filters_portable_platform_and_capability() -> None:
    assert await PlatformFilter("telegram")(event(platform="telegram"))
    assert not await PlatformFilter("bale")(event(platform="telegram"))
    assert await SupportsFilter(Feature.TEXT)(event())


@pytest.mark.asyncio
async def test_command_parses_args_and_checks_mention_against_bot() -> None:
    result = await Command("start")(event("/start hello"), bot=FakeBot())
    assert result and result["command"].args == "hello"
    result = await Command("start")(event("/start@my_bot hello"), bot=FakeBot())
    assert result and result["command"].mention == "my_bot"
    assert not await Command("start")(event("/start@other_bot"), bot=FakeBot())
    assert await CommandStart(deep_link=True)(event("/start payload"), bot=FakeBot())


class Menu(CallbackData, prefix="menu"):
    action: str
    page: int = 0


class Kind(Enum):
    A = "a"


class ComplexData(CallbackData, prefix="complex"):
    uid: UUID
    amount: Decimal
    flag: bool
    kind: Kind
    optional: str | None = None


@pytest.mark.asyncio
async def test_callback_data_round_trip_and_edge_cases() -> None:
    value = Menu("open", 2)
    assert Menu.unpack(value.pack()) == value
    result = await Menu.filter(F.action == "open")(type("Callback", (), {"data": value.pack()})())
    assert result and result["callback_data"] == value
    with pytest.raises(ValueError): Menu("a:b").pack()
    complex_value = ComplexData(UUID("00000000-0000-0000-0000-000000000001"), Decimal("1.20"), True, Kind.A)
    assert ComplexData.unpack(complex_value.pack()) == complex_value


def test_filter_algebra() -> None:
    predicate = and_f(TextEquals("x"), invert_f(TextEquals("y")))
    assert predicate is not None
    assert or_f(TextEquals("x"), TextEquals("y")) is not None


@pytest.mark.asyncio
async def test_magic_data_reads_dependency_mapping() -> None:
    assert await MagicData(F.value == 3)(event(), value=3)
    assert not await MagicData(F.value == 3)(event(), value=4)
    assert await MagicData(F["value"] == 3)(event(), value=3)
