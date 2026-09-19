Telegram API
============

The Telegram adapter contains the largest platform surface in Peyk, including
messages, media, forum topics, keyboards, inline mode, stickers, payments,
Passport, games, business accounts, boosts/gifts, web apps, and newer Telegram
features.

Client
------

.. automodule:: peyk.platforms.telegram
   :members:
   :undoc-members: false
   :show-inheritance:

Shared client methods
---------------------

Bale and Telegram inherit a small set of proven platform-neutral request methods.
They are documented here as part of each platform reference so the complete
public client surface is discoverable from either page.

.. automodule:: peyk.platforms._telegram_like.base_client
   :members:
   :undoc-members: false

Types and methods
-----------------
.. currentmodule:: peyk.platforms.telegram

.. autosummary::
   :toctree: generated/telegram
   :recursive:

   peyk.platforms.telegram.types
   peyk.platforms.telegram.methods

Supporting modules
------------------

.. automodule:: peyk.platforms.telegram.errors
   :members:
