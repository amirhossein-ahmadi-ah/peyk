from __future__ import annotations

from types import SimpleNamespace

import pytest

from peyk import Bot
from peyk.platform_core.errors import UnsupportedFeatureError


@pytest.mark.parametrize("platform", ["telegram", "bale", "rubika"])
def test_token_is_public_on_bot_and_client(platform: str) -> None:
    bot = Bot("123:ABC", platform=platform)  # type: ignore[arg-type]

    assert bot.token == "123:ABC"
    assert bot.client.token == "123:ABC"


@pytest.mark.asyncio
async def test_bale_create_chat_invite_link_returns_url() -> None:
    class FakeBale:
        async def create_chat_invite_link(self, chat_id: int | str) -> dict[str, object]:
            assert chat_id == 555
            return {"invite_link": "https://ble.ir/join/xyz"}

    bot = Bot("token", platform="bale")
    bot._client = FakeBale()  # type: ignore[assignment]

    assert await bot.create_chat_invite_link(555) == "https://ble.ir/join/xyz"


@pytest.mark.asyncio
async def test_bale_rejects_telegram_only_invite_options() -> None:
    bot = Bot("token", platform="bale")

    with pytest.raises(UnsupportedFeatureError):
        await bot.create_chat_invite_link(555, member_limit=5)


@pytest.mark.asyncio
async def test_telegram_create_chat_invite_link_forwards_options() -> None:
    seen: dict[str, object] = {}

    class FakeTelegram:
        async def create_chat_invite_link(self, chat_id: int | str, **kwargs: object) -> SimpleNamespace:
            seen.update(kwargs)
            return SimpleNamespace(invite_link="https://t.me/+abc")

    bot = Bot("token", platform="telegram")
    bot._client = FakeTelegram()  # type: ignore[assignment]

    assert await bot.create_chat_invite_link(-100, name="promo", member_limit=3) == "https://t.me/+abc"
    assert seen == {"name": "promo", "expire_date": None, "member_limit": 3, "creates_join_request": None}


@pytest.mark.asyncio
async def test_rubika_create_chat_invite_link_is_unsupported() -> None:
    bot = Bot("token", platform="rubika")

    with pytest.raises(UnsupportedFeatureError):
        await bot.create_chat_invite_link("c1")
