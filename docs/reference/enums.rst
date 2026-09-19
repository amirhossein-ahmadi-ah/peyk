Enum reference
==============

Neutral enums
-------------

The platform-neutral public enums are exposed from ``peyk.enums``:

* ``ContentType``
* ``ChatType``
* ``ChatAction``
* ``ParseMode``
* ``ButtonStyle``
* ``Platform``

Telegram enums
--------------

Telegram-specific Bot API discriminators are exposed from
``peyk.platforms.telegram.enums``. Phase 10A adds the missing command-scope,
subscription, media, rich-message, sticker, topic, transaction and update
kind enums without changing existing wire values.
