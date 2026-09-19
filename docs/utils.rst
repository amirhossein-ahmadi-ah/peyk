Utilities
=========

Flags
-----
``peyk.flags.flags`` provides aiogram-style handler decorators such as
``flags.chat_action("typing")`` and ``flags.callback_answer()``.

Chat actions
------------
``peyk.utils.chat_action.ChatActionSender`` is an async context manager for
repeated chat-action delivery. The middleware is capability-aware and does
not synthesize unsupported platform calls.

Deep links
----------
``encode_payload`` and ``decode_payload`` implement URL-safe base64 payloads.
``create_start_link`` is currently limited to Telegram because its link format
is the only audited start-link format in Peyk.

Web Apps
--------
``check_webapp_signature`` and ``safe_parse_webapp_init_data`` validate
Telegram Web App init data. Bale web-app support is intentionally absent.

Internationalization
--------------------
``I18n`` and ``I18nMiddleware`` use GNU gettext catalogs and expose
``gettext``, ``ngettext`` and ``lazy_gettext`` through dispatcher DI.
