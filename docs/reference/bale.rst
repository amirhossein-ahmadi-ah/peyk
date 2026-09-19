Bale API
========

The Bale adapter provides the typed asynchronous client and Bale-specific
request/response models.  The generated reference below recursively discovers
the restructured ``types`` and ``methods`` packages.

Client
------

.. automodule:: peyk.platforms.bale
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

.. currentmodule:: peyk.platforms.bale

.. autosummary::
   :toctree: generated/bale
   :recursive:

   peyk.platforms.bale.types
   peyk.platforms.bale.methods

Supporting modules
------------------

.. automodule:: peyk.platforms.bale.errors
   :members: