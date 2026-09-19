# Changelog

All notable changes to this project are documented in this file.

## [Unreleased]

### Fixed

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
