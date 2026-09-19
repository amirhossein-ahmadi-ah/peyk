import logging

import pytest

from peyk.dispatcher import Router, UNHANDLED
from peyk.dispatcher.filters import CallbackDataEquals, Command, TextEquals
from peyk.platform_core.contracts import (
    IncomingBotMembershipChange,
    IncomingCallbackQuery,
    IncomingChatMemberStatusUpdate,
    IncomingMessage,
    IncomingMessageDeleted,
    IncomingPreCheckoutQuery,
    IncomingShippingQuery,
)


@pytest.mark.asyncio
async def test_registration_filters_and_first_match_dispatch() -> None:
    router = Router()
    seen: list[str] = []

    @router.message(Command("start"))
    async def start(event: IncomingMessage) -> None:
        seen.append("start")

    @router.message(TextEquals("/start"))
    def exact(event: IncomingMessage) -> None:
        seen.append("exact")

    @router.callback_query(CallbackDataEquals("ok"))
    async def callback(event: IncomingCallbackQuery) -> None:
        seen.append("callback")

    await router.propagate_event(IncomingMessage(text="/start"))
    await router.propagate_event(IncomingCallbackQuery(data="ok"))
    assert seen == ["start", "callback"]


@pytest.mark.asyncio
async def test_all_normalized_contract_registration_methods_dispatch() -> None:
    router = Router()
    seen: list[str] = []

    @router.chat_member_status_update()
    async def member(event: IncomingChatMemberStatusUpdate) -> None:
        seen.append("member")

    @router.bot_membership()
    async def bot(event: IncomingBotMembershipChange) -> None:
        seen.append("bot")

    @router.message_deleted()
    async def deleted(event: IncomingMessageDeleted) -> None:
        seen.append("deleted")

    @router.pre_checkout_query()
    async def pre(event: IncomingPreCheckoutQuery) -> None:
        seen.append("pre")

    @router.shipping_query()
    async def shipping(event: IncomingShippingQuery) -> None:
        seen.append("shipping")

    await router.propagate_event(IncomingChatMemberStatusUpdate())
    await router.propagate_event(IncomingBotMembershipChange(added=True))
    await router.propagate_event(IncomingMessageDeleted(message_id=1))
    await router.propagate_event(IncomingPreCheckoutQuery(id="p"))
    await router.propagate_event(IncomingShippingQuery(id="s"))
    assert seen == ["member", "bot", "deleted", "pre", "shipping"]


@pytest.mark.asyncio
async def test_nested_routers_are_composable_and_filters_are_independent() -> None:
    parent = Router(name="parent")
    child = Router(name="child")
    parent.include_router(child)
    seen: list[str] = []

    @parent.message(TextEquals("parent"))
    async def parent_handler(event: IncomingMessage) -> None:
        seen.append("parent")

    @child.message(TextEquals("child"))
    async def child_handler(event: IncomingMessage) -> None:
        seen.append("child")

    await parent.propagate_event(IncomingMessage(text="parent"))
    assert seen == ["parent"]
    await parent.propagate_event(IncomingMessage(text="child"))
    assert seen == ["parent", "child"]


@pytest.mark.asyncio
async def test_handler_exception_goes_to_error_observer_and_stops_matching(caplog: pytest.LogCaptureFixture) -> None:
    router = Router(name="errors")
    seen: list[str] = []
    errors: list[str] = []

    @router.errors()
    async def error(event) -> None:
        errors.append(str(event.exception))

    @router.message(TextEquals("x"))
    async def failing(event: IncomingMessage) -> None:
        seen.append("failing")
        raise RuntimeError("boom")

    @router.message(TextEquals("x"))
    async def succeeding(event: IncomingMessage) -> None:
        seen.append("succeeding")

    with caplog.at_level(logging.ERROR, logger="peyk.dispatcher.router"):
        await router.propagate_event(IncomingMessage(text="x"))

    assert seen == ["failing"]
    assert errors == ["boom"]


@pytest.mark.asyncio
async def test_unknown_raw_event_is_ignored() -> None:
    router = Router()
    called = False

    @router.message()
    async def handler(event: IncomingMessage) -> None:
        nonlocal called
        called = True

    assert await router.propagate_event(object()) is UNHANDLED
    assert called is False


def test_include_router_rejects_cycles() -> None:
    a = Router()
    b = Router()
    a.include_router(b)
    with pytest.raises(ValueError):
        b.include_router(a)
