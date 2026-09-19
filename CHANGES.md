# Changelog

All notable changes to this project are documented in this file.

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
