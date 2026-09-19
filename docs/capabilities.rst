Platform capabilities
=====================

The generated capability table is maintained in ``docs/capabilities.md``.
The Markdown file is the canonical generated artifact; the table below is the
same audited information for the Sphinx site.

.. csv-table:: Audited capability summary
   :header: "Area", "Telegram", "Bale", "Rubika"
   :widths: 30, 20, 20, 30

   "messaging.text", "full", "full", "full"
   "messaging.media_group", "full", "full", "none"
   "messaging.chat_actions", "full", "full", "none"
   "callbacks.answer", "full", "full", "none"
   "updates.polling", "full", "full", "full"
   "updates.webhook", "full", "full", "partial / parameter semantics UNKNOWN"
   "files.multi_step_upload", "unknown", "unknown", "full"
   "keyboards.inline", "full", "full", "full"
   "keyboards.reply", "full", "full", "full"

See ``capabilities.md`` for the complete generated matrix and evidence notes.
