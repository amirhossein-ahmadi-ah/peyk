"""Per-platform adapters built on top of `peyk.transport`.

Each subpackage (e.g. `bale`) is a thin, typed wrapper around one bot
platform's HTTP API, sharing the generic transport layer (`Session`,
retry policy, error hierarchy, multipart, logging hook) but owning its
own platform-specific request shapes, models, and error parsing.
"""
