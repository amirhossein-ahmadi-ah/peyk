Migration from aiogram
======================

Peyk intentionally follows aiogram 3 naming and handler patterns where the semantics are shared, while adding a platform-neutral layer.

Import mapping
--------------

+----------------------+--------------------------+
| aiogram              | peyk                     |
+======================+==========================+
| ``Bot``              | ``peyk.Bot``             |
+----------------------+--------------------------+
| ``Dispatcher``       | ``peyk.Dispatcher``      |
+----------------------+--------------------------+
| ``Router``            | ``peyk.Router``          |
+----------------------+--------------------------+
| ``F``                | ``peyk.F``               |
+----------------------+--------------------------+
| ``Command``          | ``peyk.Command``         |
+----------------------+--------------------------+
| ``CallbackData``     | ``peyk.CallbackData``    |
+----------------------+--------------------------+
| keyboard builders    | ``peyk.keyboard``        |
+----------------------+--------------------------+

What is intentionally identical
--------------------------------

The main Bot/Dispatcher/Router shape, decorator handlers, filters, state groups, keyboard builders, callback-data packing, and neutral formatting are designed around aiogram 3 usage patterns.

What differs
------------

* A bot is created with ``platform="telegram" | "bale" | "rubika"``. Application handlers do not carry platform names.
* Incoming and outgoing values use neutral Peyk objects where a cross-platform contract exists.
* ``.raw`` remains an explicit escape hatch to the native platform object.
* ``bot.client`` exposes the selected native client when an application needs a platform-specific API.
* Unsupported capabilities follow the documented degrade/raise policy instead of being silently assumed to exist everywhere.
* The ``message`` observer is for normalized message events; Telegram edited/channel-post events have dedicated observers.

Compatibility shims
-------------------

Legacy import paths retained by the project remain available where documented. Deprecated shims emit ``DeprecationWarning`` and are scheduled for removal only in a future breaking release; no removal is part of this release.
