<p align="center">
  <img src="assets/logo.svg" alt="peyk logo" width="160">
</p>

<h1 align="center">peyk</h1>

<p align="center">An aiogram-style async bot library for Telegram, Bale, and Rubika.</p>

## 10-line quickstart

```python
from peyk import Bot

bot = Bot("TOKEN", platform="telegram")

@bot.command("start")
async def start(message):
    await message.answer("Hello from peyk!")

@bot.message()
async def echo(message):
    await message.answer(message.text or "")

bot.run()
```

`platform=` is selected once when the bot is created; handlers, filters, keyboards, and normalized message objects stay platform-neutral.

## Install

```bash
pip install peyk
```

For development:

```bash
pip install -e ".[dev]"
```

## Documentation

- [Capabilities](docs/capabilities.md) — audited feature support and UNKNOWN areas.
- [Migration from aiogram](docs/migration_aiogram.rst) — import mapping, compatible surfaces, and Peyk-specific differences.
- [Quickstart](docs/quickstart.rst) — simple `bot.run()` first, then Dispatcher/Router.
- [Examples](examples/) — runnable examples using public imports.

## Tests

```bash
pytest
```

The test suite is offline and uses local/fake servers and in-memory/fakeredis fixtures.

## Project record

See `docs/decisions.md` for the architectural decision record and capability evidence.

## Publishing

See [`PUBLISHING.md`](PUBLISHING.md) for the one-time GitHub/PyPI setup and
the release checklist for every version after that.

## License

MIT — see [`LICENSE`](LICENSE).
