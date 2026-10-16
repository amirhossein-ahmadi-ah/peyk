# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Added

- **Soroush Plus (Splus) platform.** `SplusBot` / `Bot(token, platform="splus")` and
  `peyk.platforms.splus.SplusClient` talk to `https://api.splus.ir/bot<TOKEN>/<method>`, a
  Telegram-shaped bot API (long polling and webhooks, inline/reply keyboards, callback queries). Models and operation strategies are shared with Telegram;
  only the methods that the official Splus documentation lists are bound on `SplusClient`
  (`SPLUS_METHODS`). Capabilities are declared in `platform_core/capabilities/splus.py`: confirmed
  features are `FULL`, features the Splus models positively lack (polls, venues, payments, inline
  mode, member-status updates, webhook secret header) are `NONE`, everything unverified (chat
  administration, button colours, ...) stays `UNKNOWN` and is refused by `Bot` until probed.
  `reply_parameters` / `link_preview_options` are rewritten to the classic
  `reply_to_message_id` / `disable_web_page_preview` fields at request level. Webhooks are
  authenticated by the secret URL path (Splus has no `secret_token`). See `docs/decisions.md`
  ("Splus platform") and `scripts/probe_splus.py` to verify the open points against a live bot.
- Bale polls (an update kind that is in the live API but missing from Bale's docs; modelled on
  pyrobale): new `bale.Poll` / `bale.PollOption` types, `Message.poll` is now parsed (so
  `ContentType.POLL` works for Bale messages), and `Update.poll` is parsed and delivered to the
  `@router.poll()` observer on Bale bots. Sending polls on Bale is still unsupported.

### Fixed

- Multipart media uploads (bytes/streams, e.g. Bale `send_animation` with downloaded GIF bytes) sent
  `reply_markup` as the Python `repr()` of the keyboard dataclass, so the platform dropped the inline
  keyboard. Dataclass models and tuples are now JSON-encoded in form fields
  (`TelegramLikeClient._form_field_value`, also used by the Telegram file-message path).
- `Bot.create_chat_invite_link()` now exists on the platform-neutral `Bot`; it returned
  `AttributeError` even though the Bale/Telegram clients implemented it. It returns the
  invite URL as a `str`. `name`, `expire_date`, `member_limit` and `creates_join_request`
  are Telegram-only and raise `UnsupportedFeatureError` on Bale; Rubika is unsupported.
- The bot token is now readable: `bot.token` and `bot.client.token` (Bale, Telegram and
  Rubika). Previously only the private `_token` attribute existed.
- `Router.command()` (and therefore `Dispatcher.command()`) now exists; only
  `Bot.command()` did, so three shipped examples crashed on load.
- `F` (magic-filter) expressions passed to `@router.message(...)`,
  `Command(magic=...)` and `CallbackData.filter(...)` matched every event
  because the object was called instead of resolved.
- Telegram polling and webhook registration now always send an explicit
  `allowed_updates` list (`Dispatcher.resolve_used_update_types()`). Telegram
  remembers the previous value per token, which could silently drop
  `callback_query` and `inline_query` updates.
- `FSMContextMiddleware` no longer fails updates that have no chat/user
  (for example an unhandled `inline_query`).
- `I18nMiddleware` now gets the user's language: the neutral `User` was
  missing `language_code`. `gettext` is bound to the event's locale, so
  concurrent handlers cannot switch each other's language.
- `examples/i18n.py` ships a real `locales/` catalog; `examples/dispatcher_router.py`
  includes the `admin` router before the catch-all one.

## [1.0.0] — Initial public release

- First public release of `peyk`: an aiogram-style, async, multi-platform bot
  library supporting Telegram, Bale, and Rubika through one shared API.
- Shared transport layer (tuned `aiohttp` session, `orjson`, retry/backoff).
- Full Bale and Telegram client coverage, with a shared `TelegramLikeClient`
  base extracted from both real implementations.
- Rubika client covering its full (~19-method) API surface, including its
  webhook secret-key verification and chat-keypad/inline-keypad button types.
- Platform-agnostic dispatcher: `Router`/`Filter` composition, middleware,
  and an FSM with in-memory and Redis storage backends.
- Platform-aware text formatting and keyboard-building helpers.
- Full test suite running offline against local fake servers — no real
  network calls required to run the tests.
