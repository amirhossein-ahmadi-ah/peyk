"""Tests for `TelegramClient` bot commands & bot profile (Phase T8).

Fake `aiohttp.test_utils` server, zero real network. Covers one
happy-path test per T8 method, `BotCommandScope` serialization across
multiple subtypes as an outgoing parameter, all three `MenuButton`
subtypes round-tripping, and `language_code` omitted vs. explicit
empty string vs. a real code.
"""

from __future__ import annotations

from typing import Any, Callable, Dict

import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    BotCommand,
    BotCommandScopeAllPrivateChats,
    BotCommandScopeChat,
    BotCommandScopeChatAdministrators,
    BotCommandScopeChatMember,
    BotCommandScopeDefault,
    BotDescription,
    BotName,
    BotShortDescription,
    ChatAdministratorRights,
    MenuButtonCommands,
    MenuButtonDefault,
    MenuButtonWebApp,
    WebAppInfo,
    parse_bot_command_scope,
    parse_menu_button,
    serialize_bot_command_scope,
    serialize_menu_button,
)
from peyk.transport import RetryPolicy

TOKEN = "12345:TEST-TOKEN"


class FakeTelegramServer:
    def __init__(self) -> None:
        self.responses: Dict[str, Callable[[Any], Any]] = {}
        self.request_log: list[Dict[str, Any]] = []
        self.app = web.Application()
        self.app.router.add_route("*", "/bot{token}/{method}", self._handle)

    def set_response(
        self, method_name: str, result_builder: Callable[[Any], Any]
    ) -> None:
        self.responses[method_name] = result_builder

    async def _handle(self, request: web.Request) -> web.Response:
        import orjson

        method_name = request.match_info["method"]
        token = request.match_info["token"]
        raw = await request.read()
        parsed_body: Any = orjson.loads(raw) if raw else {}
        self.request_log.append(
            {
                "method_name": method_name,
                "token": token,
                "http_method": request.method,
                "body": parsed_body,
            }
        )
        builder = self.responses.get(method_name)
        result = builder(parsed_body) if builder else None
        return web.json_response({"ok": True, "result": result})

    def calls_for(self, method_name: str) -> list[Dict[str, Any]]:
        return [c for c in self.request_log if c["method_name"] == method_name]


@pytest.fixture
async def fake_server():
    server = FakeTelegramServer()
    async with TestServer(server.app) as test_server:
        yield server, test_server


def _client_for(
    test_server: TestServer, server: FakeTelegramServer
) -> TelegramClient:
    base_url = str(test_server.make_url("")).rstrip("/")
    return TelegramClient(
        TOKEN,
        base_url=base_url,
        retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.001),
    )


SAMPLE_COMMANDS = [
    {"command": "start", "description": "Start the bot"},
    {"command": "help", "description": "Show help", "is_ephemeral": True},
]


# -- set_my_commands --------------------------------------------------------


async def test_set_my_commands_basic(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setMyCommands", lambda body: True)
    client = _client_for(test_server, server)

    assert (
        await client.set_my_commands(
            [
                BotCommand(command="start", description="Start the bot"),
                {"command": "help", "description": "Show help"},
            ]
        )
        is True
    )

    (call,) = server.calls_for("setMyCommands")
    assert call["body"] == {
        "commands": [
            {"command": "start", "description": "Start the bot"},
            {"command": "help", "description": "Show help"},
        ]
    }


async def test_set_my_commands_with_scope_and_language(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setMyCommands", lambda body: True)
    client = _client_for(test_server, server)

    assert (
        await client.set_my_commands(
            [BotCommand(command="start", description="Start")],
            scope=BotCommandScopeChat(chat_id=12345),
            language_code="fa",
        )
        is True
    )

    (call,) = server.calls_for("setMyCommands")
    assert call["body"] == {
        "commands": [{"command": "start", "description": "Start"}],
        "scope": {"type": "chat", "chat_id": 12345},
        "language_code": "fa",
    }


async def test_set_my_commands_scope_all_private_chats(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setMyCommands", lambda body: True)
    client = _client_for(test_server, server)

    assert (
        await client.set_my_commands(
            [BotCommand(command="ping", description="Ping")],
            scope=BotCommandScopeAllPrivateChats(),
        )
        is True
    )

    (call,) = server.calls_for("setMyCommands")
    assert call["body"]["scope"] == {"type": "all_private_chats"}
    assert "language_code" not in call["body"]


async def test_set_my_commands_scope_chat_member_raw_mapping(
    fake_server,
) -> None:
    server, test_server = fake_server
    server.set_response("setMyCommands", lambda body: True)
    client = _client_for(test_server, server)

    assert (
        await client.set_my_commands(
            [BotCommand(command="mod", description="Mod tools")],
            scope=BotCommandScopeChatMember(chat_id=-1001, user_id=777),
        )
        is True
    )

    (call,) = server.calls_for("setMyCommands")
    assert call["body"]["scope"] == {
        "type": "chat_member",
        "chat_id": -1001,
        "user_id": 777,
    }


async def test_set_my_commands_empty_language_string_passes_through(
    fake_server,
) -> None:
    # Omitted (None) and explicit "" stay distinguishable on the wire;
    # per the live docs both mean "default language" server-side.
    server, test_server = fake_server
    server.set_response("setMyCommands", lambda body: True)
    client = _client_for(test_server, server)

    await client.set_my_commands(
        [BotCommand(command="start", description="Start")], language_code=""
    )

    (call,) = server.calls_for("setMyCommands")
    assert call["body"]["language_code"] == ""


# -- get_my_commands / delete_my_commands ------------------------------------


async def test_get_my_commands_parses_list(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("getMyCommands", lambda body: SAMPLE_COMMANDS)
    client = _client_for(test_server, server)

    commands = await client.get_my_commands()
    assert commands == [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(
            command="help", description="Show help", is_ephemeral=True
        ),
    ]

    (call,) = server.calls_for("getMyCommands")
    assert call["body"] == {}


async def test_get_my_commands_with_scope_and_language(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("getMyCommands", lambda body: [])
    client = _client_for(test_server, server)

    assert (
        await client.get_my_commands(
            scope=BotCommandScopeChatAdministrators(chat_id="@group"),
            language_code="en",
        )
        == []
    )

    (call,) = server.calls_for("getMyCommands")
    assert call["body"] == {
        "scope": {"type": "chat_administrators", "chat_id": "@group"},
        "language_code": "en",
    }


async def test_delete_my_commands_with_scope_and_language(
    fake_server,
) -> None:
    server, test_server = fake_server
    server.set_response("deleteMyCommands", lambda body: True)
    client = _client_for(test_server, server)

    assert (
        await client.delete_my_commands(
            scope=BotCommandScopeDefault(), language_code="fa"
        )
        is True
    )

    (call,) = server.calls_for("deleteMyCommands")
    assert call["body"] == {
        "scope": {"type": "default"},
        "language_code": "fa",
    }


async def test_delete_my_commands_defaults(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("deleteMyCommands", lambda body: True)
    client = _client_for(test_server, server)

    assert await client.delete_my_commands() is True

    (call,) = server.calls_for("deleteMyCommands")
    assert call["body"] == {}


# -- bot name ---------------------------------------------------------------


async def test_set_my_name_with_language(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setMyName", lambda body: True)
    client = _client_for(test_server, server)

    assert await client.set_my_name(name="ربات من", language_code="fa") is True

    (call,) = server.calls_for("setMyName")
    assert call["body"] == {"name": "ربات من", "language_code": "fa"}


async def test_set_my_name_removes_with_empty_string(fake_server) -> None:
    # Empty name removes the dedicated name for the given language.
    server, test_server = fake_server
    server.set_response("setMyName", lambda body: True)
    client = _client_for(test_server, server)

    assert await client.set_my_name(name="", language_code="fa") is True

    (call,) = server.calls_for("setMyName")
    assert call["body"] == {"name": "", "language_code": "fa"}


async def test_get_my_name_without_language(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("getMyName", lambda body: {"name": "My Bot"})
    client = _client_for(test_server, server)

    result = await client.get_my_name()
    assert isinstance(result, BotName)
    assert result.name == "My Bot"

    (call,) = server.calls_for("getMyName")
    assert call["body"] == {}


async def test_get_my_name_with_language(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("getMyName", lambda body: {"name": "ربات من"})
    client = _client_for(test_server, server)

    result = await client.get_my_name(language_code="fa")
    assert result is not None and result.name == "ربات من"

    (call,) = server.calls_for("getMyName")
    assert call["body"] == {"language_code": "fa"}


# -- bot description / short description -------------------------------------


async def test_set_and_get_my_description(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setMyDescription", lambda body: True)
    server.set_response(
        "getMyDescription", lambda body: {"description": "Does things"}
    )
    client = _client_for(test_server, server)

    assert await client.set_my_description(description="Does things") is True
    (call,) = server.calls_for("setMyDescription")
    assert call["body"] == {"description": "Does things"}

    result = await client.get_my_description(language_code="en")
    assert isinstance(result, BotDescription)
    assert result.description == "Does things"
    (call,) = server.calls_for("getMyDescription")
    assert call["body"] == {"language_code": "en"}


async def test_set_and_get_my_short_description(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setMyShortDescription", lambda body: True)
    server.set_response(
        "getMyShortDescription", lambda body: {"short_description": "Short"}
    )
    client = _client_for(test_server, server)

    assert (
        await client.set_my_short_description(
            short_description="Short", language_code="en"
        )
        is True
    )
    (call,) = server.calls_for("setMyShortDescription")
    assert call["body"] == {
        "short_description": "Short",
        "language_code": "en",
    }

    result = await client.get_my_short_description()
    assert isinstance(result, BotShortDescription)
    assert result.short_description == "Short"
    (call,) = server.calls_for("getMyShortDescription")
    assert call["body"] == {}


# -- menu button -------------------------------------------------------------


async def test_set_chat_menu_button_web_app(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setChatMenuButton", lambda body: True)
    client = _client_for(test_server, server)

    assert (
        await client.set_chat_menu_button(
            chat_id=12345,
            menu_button=MenuButtonWebApp(
                text="Open", web_app=WebAppInfo(url="https://example.com/app")
            ),
        )
        is True
    )

    (call,) = server.calls_for("setChatMenuButton")
    assert call["body"] == {
        "chat_id": 12345,
        "menu_button": {
            "type": "web_app",
            "text": "Open",
            "web_app": {"url": "https://example.com/app"},
        },
    }


async def test_set_chat_menu_button_defaults(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setChatMenuButton", lambda body: True)
    client = _client_for(test_server, server)

    assert await client.set_chat_menu_button() is True

    (call,) = server.calls_for("setChatMenuButton")
    assert call["body"] == {}


async def test_get_chat_menu_button_commands(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getChatMenuButton", lambda body: {"type": "commands"}
    )
    client = _client_for(test_server, server)

    result = await client.get_chat_menu_button(chat_id=12345)
    assert isinstance(result, MenuButtonCommands)
    assert result.type == "commands"

    (call,) = server.calls_for("getChatMenuButton")
    assert call["body"] == {"chat_id": 12345}


def test_menu_button_all_subtypes_round_trip() -> None:
    for raw in (
        {"type": "commands"},
        {
            "type": "web_app",
            "text": "Play",
            "web_app": {"url": "https://example.com/game"},
        },
        {"type": "default"},
    ):
        parsed = parse_menu_button(raw)
        assert parsed is not None
        assert serialize_menu_button(parsed) == raw

    assert isinstance(parse_menu_button({"type": "commands"}), MenuButtonCommands)
    web_app = parse_menu_button(
        {
            "type": "web_app",
            "text": "Play",
            "web_app": {"url": "https://example.com/game"},
        }
    )
    assert isinstance(web_app, MenuButtonWebApp)
    assert web_app.web_app is not None
    assert web_app.web_app.url == "https://example.com/game"
    assert isinstance(parse_menu_button({"type": "default"}), MenuButtonDefault)


# -- default administrator rights --------------------------------------------


async def test_set_my_default_administrator_rights(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("setMyDefaultAdministratorRights", lambda body: True)
    client = _client_for(test_server, server)

    assert (
        await client.set_my_default_administrator_rights(
            rights=ChatAdministratorRights(
                can_delete_messages=True, can_invite_users=True
            ),
            for_channels=True,
        )
        is True
    )

    (call,) = server.calls_for("setMyDefaultAdministratorRights")
    assert call["body"] == {
        "rights": {
            "can_delete_messages": True,
            "can_invite_users": True,
        },
        "for_channels": True,
    }


async def test_set_my_default_administrator_rights_clears(
    fake_server,
) -> None:
    # Omitting `rights` clears the default rights (per the docs).
    server, test_server = fake_server
    server.set_response("setMyDefaultAdministratorRights", lambda body: True)
    client = _client_for(test_server, server)

    assert await client.set_my_default_administrator_rights() is True

    (call,) = server.calls_for("setMyDefaultAdministratorRights")
    assert call["body"] == {}


async def test_get_my_default_administrator_rights(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getMyDefaultAdministratorRights",
        lambda body: {"can_delete_messages": True, "can_manage_chat": False},
    )
    client = _client_for(test_server, server)

    result = await client.get_my_default_administrator_rights(
        for_channels=False
    )
    assert isinstance(result, ChatAdministratorRights)
    assert result.can_delete_messages is True
    assert result.can_manage_chat is False

    (call,) = server.calls_for("getMyDefaultAdministratorRights")
    assert call["body"] == {"for_channels": False}


# -- union serialization helpers ----------------------------------------------


def test_bot_command_scope_serialization_subtypes() -> None:
    assert serialize_bot_command_scope(BotCommandScopeDefault()) == {
        "type": "default"
    }
    assert serialize_bot_command_scope(BotCommandScopeAllPrivateChats()) == {
        "type": "all_private_chats"
    }
    assert serialize_bot_command_scope(
        BotCommandScopeChat(chat_id="@channel")
    ) == {"type": "chat", "chat_id": "@channel"}
    assert serialize_bot_command_scope(
        BotCommandScopeChatMember(chat_id=-1001, user_id=42)
    ) == {"type": "chat_member", "chat_id": -1001, "user_id": 42}
    # Raw mappings pass through for forward-compat.
    assert serialize_bot_command_scope({"type": "default"}) == {
        "type": "default"
    }


def test_parse_bot_command_scope_round_trip() -> None:
    for raw in (
        {"type": "default"},
        {"type": "all_private_chats"},
        {"type": "chat", "chat_id": 99},
        {
            "type": "chat_member",
            "chat_id": -1001,
            "user_id": 42,
        },
    ):
        parsed = parse_bot_command_scope(raw)
        assert parsed is not None
        assert serialize_bot_command_scope(parsed) == raw
