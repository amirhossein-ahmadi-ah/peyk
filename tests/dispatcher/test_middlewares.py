from __future__ import annotations

import logging

import pytest

from peyk.dispatcher import Router
from peyk.dispatcher.middlewares import LoggingMiddleware
from peyk.platform_core.contracts import IncomingMessage


class TraceMiddleware:
    def __init__(self, name: str, trace: list[str], *, inject: bool = False) -> None:
        self.name = name
        self.trace = trace
        self.inject = inject

    async def __call__(self, handler, event, data):
        self.trace.append(f"{self.name}:before")
        if self.inject:
            data["token"] = "injected"
        try:
            return await handler()
        finally:
            self.trace.append(f"{self.name}:after")


@pytest.mark.asyncio
async def test_three_middlewares_wrap_dispatch_in_registration_order() -> None:
    router = Router()
    trace: list[str] = []
    router.middleware(TraceMiddleware("m1", trace))
    router.middleware(TraceMiddleware("m2", trace))
    router.middleware(TraceMiddleware("m3", trace))

    @router.message()
    async def handler(event: IncomingMessage) -> None:
        trace.append("handler")

    await router.propagate_event(IncomingMessage(text="hello"))
    assert trace == [
        "m1:before", "m2:before", "m3:before",
        "handler",
        "m3:after", "m2:after", "m1:after",
    ]


@pytest.mark.asyncio
async def test_middleware_data_is_injected_into_handler() -> None:
    router = Router()
    router.middleware(TraceMiddleware("injector", [], inject=True))
    received: list[str] = []

    @router.message()
    async def handler(event: IncomingMessage, token: str) -> None:
        received.append(token)

    await router.propagate_event(IncomingMessage(text="hello"))
    assert received == ["injected"]


@pytest.mark.asyncio
async def test_middleware_runs_even_when_no_handler_matches() -> None:
    router = Router()
    trace: list[str] = []
    router.middleware(TraceMiddleware("outer", trace))

    await router.propagate_event(IncomingMessage(text="unmatched"))
    assert trace == ["outer:before", "outer:after"]


@pytest.mark.asyncio
async def test_middleware_failure_does_not_break_sibling_handlers(caplog) -> None:
    router = Router(name="middleware-errors")
    seen: list[str] = []

    class FailingMiddleware:
        async def __call__(self, handler, event, data):
            raise RuntimeError("middleware boom")

    router.middleware(FailingMiddleware())

    @router.message()
    async def first(event: IncomingMessage) -> None:
        seen.append("first")

    @router.message()
    async def second(event: IncomingMessage) -> None:
        seen.append("second")

    with caplog.at_level(logging.ERROR, logger="peyk.dispatcher.router"):
        await router.propagate_event(IncomingMessage(text="x"))

    assert seen == []
    assert "Unhandled exception in router" in caplog.text


@pytest.mark.asyncio
async def test_handler_failure_remains_isolated_with_middleware() -> None:
    router = Router()
    trace: list[str] = []
    router.middleware(TraceMiddleware("m", trace))
    seen: list[str] = []

    @router.message()
    async def failing(event: IncomingMessage) -> None:
        seen.append("failing")
        raise RuntimeError("handler boom")

    @router.message()
    async def succeeding(event: IncomingMessage) -> None:
        seen.append("succeeding")

    await router.propagate_event(IncomingMessage(text="x"))
    assert seen == ["failing"]
    assert trace == ["m:before", "m:after"]


@pytest.mark.asyncio
async def test_logging_middleware_logs_all_three_normalized_platform_shapes(caplog) -> None:
    from peyk.platform_core.adapters.bale import normalize_message as normalize_bale
    from peyk.platform_core.adapters.rubika import normalize_message as normalize_rubika
    from peyk.platform_core.adapters.telegram import normalize_message as normalize_telegram
    from peyk.platforms.bale.models import Chat as BaleChat, Message as BaleMessage, User as BaleUser
    from peyk.platforms.rubika.models import Message as RubikaMessage
    from peyk.platforms.telegram.models import Chat as TelegramChat, Message as TelegramMessage, User as TelegramUser

    router = Router()
    router.middleware(LoggingMiddleware())
    count = 0

    @router.message()
    async def handler(event: IncomingMessage) -> None:
        nonlocal count
        count += 1

    events = [
        normalize_telegram(TelegramMessage(
            message_id=1, date=1,
            chat=TelegramChat(id=10, type="private"),
            from_=TelegramUser(id=11, is_bot=False, first_name="T"),
            text="hello",
        )),
        normalize_bale(BaleMessage(
            message_id=1, date=1,
            chat=BaleChat(id=10, type="private"),
            from_=BaleUser(id=11, is_bot=False, first_name="B"),
            text="hello",
        )),
        normalize_rubika(RubikaMessage(
            message_id="1", text="hello", sender_id="11", time=1,
        )),
    ]

    with caplog.at_level(logging.INFO, logger="peyk.transport"):
        for event in events:
            await router.propagate_event(event)

    assert count == 3
    assert caplog.messages.count("event: IncomingMessage") == 3
