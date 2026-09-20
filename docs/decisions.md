# Consolidated Merge Decisions — M1–M6

## 1. Project boundary and transport

`peyk` is a standalone shared transport/client project. It has its own
`pyproject.toml` and does not depend on `hazardastan`. The transport layer is
platform-neutral and uses a reusable `aiohttp` session with an explicit
connection pool configuration (`limit=100`, `limit_per_host=30`,
`keepalive_timeout=30s`, `ttl_dns_cache=300s`). These values are intentional
workload knobs for a long-lived, bursty bot client; they are not copied from a
specific bot library.

`Session.request()` uses a single total-duration `aiohttp.ClientTimeout` and
supports JSON and multipart requests. Multipart file-like objects are handed
to `aiohttp` rather than read into memory by `peyk`. `Retry-After` parsing in
the generic transport handles only delta-seconds; richer/platform-specific
interpretation remains above the transport layer.

Transport logging is split deliberately: request logging occurs per attempt
in `Session`, while retry/final-failure logging lives in `run_with_retry` so
retries are not double-logged. The default transport logger is a lazy
module-level singleton.

Connection-refused tests use an OS-assigned unused local port rather than a
hard-coded low port, and accept either the connection error or client timeout
where Windows networking/security software can change the observed failure.

## 2. Platform adapters before the merge

Bale and Telegram were completed independently before common code was
extracted. Both clients use the same `ok`/`result`/`description`/
`error_code` response envelope, but they own their own models and error
classes.

The Bale adapter intentionally POSTs every API call. Its API `close` method is
exposed as `close_bot()` because `close()` already means closing the local
transport session. Bale media inputs use the two-way practical dispatch of a
string reference versus uploaded content. Bale's documented callback-data
limit is validated as 1–64 UTF-8 bytes.

Telegram retains Telegram-specific response parsing and method signatures.
In particular, application-level `parameters.retry_after` becomes a
`RateLimitedError` after transport retry handling has completed; it is not
blindly replayed by the generic transport. Telegram's richer request,
keyboard, media, inline, payment, business, story, game, passport, gift,
web-app, rich-message, ephemeral-message and other surfaces remain in the
Telegram adapter/models where their schemas differ.

## 3. M1 classification rule

The M1 comparison classified same-name operations using four buckets:

- **A — identical reusable logic:** safe to share without changing either
  public contract.
- **B — same broad operation, but materially different contract:** keep the
  public method platform-owned; only independently proven internal mechanics
  may be shared.
- **C — platform-specific operation:** no common public method exists or the
  semantics are materially platform-owned.
- **D — intentionally not shared / insufficient evidence:** do not abstract
  merely because code looks similar.

M1 found only 15 public methods to be genuinely A-level candidates. Most
same-name public methods were B, so the merge intentionally favors a narrow
shared base rather than a large artificial abstraction.

## 4. M2 shared base

`TelegramLikeClient` was introduced as the common base for Bale and Telegram.
It owns token/session/retry setup, common POST/envelope handling, and proven
shared request mechanics. It does not import either concrete platform.

The base exposes platform hooks for response models and error behavior. This
keeps model classes separate even when a method's request mechanics are
identical.

## 5. M3 — shared core methods

The first public A-level migration moved these methods into
`TelegramLikeClient`:

- `get_me`
- `get_webhook_info`
- `delete_message`

`user_model` and `webhook_info_model` preserve each platform's response model.
Telegram's retry-hint behavior remains an override rather than being encoded
into the base.

## 6. M4 — shared file/media mechanics

`get_file` is shared because both platforms make the same request and return
a platform-specific `File` model. The base therefore uses `file_model`.

Public media methods remain platform-owned because their signatures and
options differ. The base shares only the proven mechanics:

- string file references remain ordinary JSON values;
- bytes, streams and `FilePayload` values become multipart uploads;
- extra upload fields participate in the multipart decision;
- upload values are normalized to `FilePayload` with deterministic filenames;
- structured values can be serialized into multipart string fields.

`InputMedia*` families and Telegram-only media features are not merged.

## 7. M5 — chat administration and keyboards

The shared chat-administration methods are the A-level subset:

- `unban_chat_member`
- `unpin_all_chat_messages`
- `leave_chat`
- `get_chat`
- `get_chat_member`
- `_get_chat_member_count`
- `set_chat_title`
- `delete_chat_photo`

The public member-count spelling stays platform-owned (`get_chat_members_count`
on Bale and `get_chat_member_count` on Telegram), while the common request
mechanics are shared. Chat/member parsing is delegated to platform hooks.

B-classified admin methods remain in the concrete adapters because their
parameters or return models differ. Telegram-only rights-heavy administration
also remains local.

Keyboard sharing is deliberately limited to the common button payload and
UTF-8 callback-data validation. Telegram's richer `InlineKeyboardButton`
fields are not forced into Bale, and the platform-specific helper functions
still return their native model shapes.

## 8. M6 final duplication sweep

The final sweep checked both concrete clients for same-name methods and
request-building logic that could have escaped M1–M5. No new A-level public
method was justified. The remaining same-name operations are B/C/D cases
because at least one of their signatures, parameter sets, result models,
serialization rules, or platform semantics differs.

The sweep also found two concrete-code cleanup issues that were safe to
resolve without changing the intended platform boundary:

1. `TelegramClient` contained a second set of 15 method definitions appended
   later in the class. Python silently used the later definitions, which could
   hide the fuller T18 implementations and create signature drift. The
   duplicate definitions were consolidated into one implementation per
   method. Existing legacy test-call shapes that were already intentionally
   supported were retained as compatibility parameters where necessary.
2. Both concrete clients still contained copies of the same private media
   helpers (`_is_upload`, `_as_file_payload`, `_json_field`) even though M4
   had already moved those mechanics into `TelegramLikeClient`. The concrete
   copies were removed and callers now use the inherited shared helpers.

No platform-specific model classes were merged as part of this cleanup.

## 9. Final concrete-client shape

After M6, `BaleClient` and `TelegramClient` inherit the common lifecycle,
request/envelope, shared A-level method, media-mechanics and callback-data
logic from `TelegramLikeClient`.

The concrete classes retain platform-specific API methods, models, error
classes, serialization rules and documented quirks. Bale supplies its base
URL and model/parser hooks. Telegram supplies its base URL, model/parser hooks
and its application-level retry-hint behavior. Neither concrete client
imports the other.

## 10. Verification

The combined test suite covering `_telegram_like`, Bale, Telegram and
transport passes with **492 tests passed**. Tests use local/fake servers and
do not make real platform API calls.

A package-install attempt was also checked, but the sandbox cannot download
build dependencies because outbound package-network access is unavailable;
this is an environment limitation, not a test failure. The source tree was
compiled successfully with `compileall`.

## 11. Handoff

M6 is the final Bale/Telegram merge phase. The next roadmap phase is the
shared dispatcher + filters + keyboard-builder-helper work. Future adapters
such as Rubika should consume the narrow shared contracts rather than moving
platform-specific models into `TelegramLikeClient` without fresh comparative
proof.

## Rubika — Final architectural conclusion (R6, verified against official docs)

**منبع نهایی:** سایت رسمی `rubika.ir/botapi`, `botapi/methods`, `botapi/models` (اسکرپ‌شده در 2026-09-18).

### تصحیحات مهم R6 نسبت به R1–R5

R1–R5 بر اساس کتابخانه‌های ثالث چند فرض اشتباه ساختند. R6 همه را با سایت رسمی تصحیح کرد:

1. **`banUser` / `unbanUser` وجود ندارند** → نام درست `banChatMember` / `unbanChatMember` است.
2. **`setSecretKey` / `checkSecretKey` وجود ندارند** — سایت رسمی هیچ مکانیزم secret key برای وبهوک مستند نکرده.
3. **`leaveChat` وجود ندارد.**
4. **`updateBotEndpoint` (مفرد) وجود ندارد** → نام درست `updateBotEndpoints` (جمع) با پارامتر `type` (از `UpdateEndpointTypeEnum`).
5. **`setChatKeypad` وجود ندارد** → متد واحد `editChatKeypad` با `chat_keypad_type` ∈ {"New", "Remove"}.
6. **`editInlineKeypad`** — URL واقعی همین است، ولی heading سایت `editMessageKeypad` است. ما URL را استفاده می‌کنیم.
7. **`sendPhoto` / `sendVideo` / `sendDocument` / `sendVoice` / `sendMusic` وجود ندارند** → یک متد واحد `sendFile(chat_id, file_id, ...)`.
8. **`uploadFile` وجود ندارد** → جریان سه‌مرحله‌ای: `requestSendFile(type)` → `upload_url` → POST فایل به آن → `file_id` → `sendFile(chat_id, file_id)`.
9. **`sendPoll` / `sendLocation` / `sendContact` / `setCommands` / `getFile` / `requestSendFile` جا افتاده بودند** → الان اضافه شده‌اند.
10. **`getUpdates` پارامتر `offset_id` (نه `start_id`)** و خروجی `{updates, next_offset_id}` است.
11. **پاسخ‌ها معمولاً wrapped هستند:** `{"bot": {...}}`, `{"chat": {...}}` و... (نه bare object).
12. **ساختار Button تودرتو است:** `button_calendar`, `button_textbox` و... (نه فیلدهای flat).
13. **`ButtonCalendar.type` مقادیر `DatePersian` / `DateGregorian`** (نه "Persian" / "Gregorian").

### نتیجه‌ی نهایی معماری

**RubikaClient کاملاً مستقل از TelegramLikeClient می‌ماند.** با ۱۹ متد رسمی و مدل‌های منحصربه‌فرد، هیچ A-level candidate برای اشتراک پیدا نشد. دلایل ساختاری:

1. **Envelope:** `status`/`data` vs `ok`/`result` — متفاوت.
2. **Error code:** رشته‌ای vs عددی — متفاوت.
3. **ساختار Button:** تودرتو با sub-objects (vs flat).
4. **Callback shape:** `aux_data.button_id` vs `callback_data`.
5. **File upload:** سه‌مرحله‌ای (`requestSendFile` → POST → `sendFile`).
6. **Update delivery:** dual-mode (polling + webhook) با `updateBotEndpoints` که در Bale/Telegram معادل ندارد.

### لیست باقیمانده LOW-confidence (نیاز به توکن زنده برای تأیید نهایی)

- نام دقیق پارامترها در `updateBotEndpoints` (سایت `url` و `type` را نشان می‌دهد، ولی نوع دقیق `type` string enum است).
- URL نهایی `editInlineKeypad` vs `editMessageKeypad` — سایت متناقض است.
- نام دقیق فیلد multipart در `upload_url` (`file` تأییدشده از سایت).
- ساختار خطای `upload_url` POST — سایت نمی‌گوید خطاها چطور برمیگردند.

## Dispatcher D1 — raw-to-normalized adapter implementation (2026-09-18)

D1 implements the D0 normalized contracts without changing the existing
platform clients. The normalized IDs use `int | str`: Telegram and Bale keep
their integer IDs, while Rubika keeps its documented string IDs. This avoids
silently changing identifier values while still giving the dispatcher one
field name and one scalar type union.

### IncomingMessage

`IncomingMessage` contains `message_id`, `chat_id`, `sender_id`, `text`,
`date`, `is_edited`, `reply_to_message_id`, `media`,
`new_chat_members`, `left_chat_member`, `successful_payment`, and `raw`.
A missing platform field remains `None`. For media captions, `text` is the
message text when present, otherwise the caption. `media` is the first
available documented media/content object and remains platform-native; the
complete original message is always available through `raw`.

Rubika's `Message` model has no `chat_id`; `normalize_message()` therefore
leaves it `None` unless the enclosing `Update.chat_id` is supplied by the
adapter's update normalization path. Rubika also has no confirmed
`successful_payment`, `new_chat_members`, or `left_chat_member` message
fields, so these remain `None`.

### IncomingCallbackQuery

The common callback payload is `data`. Telegram and Bale map their
`CallbackQuery.data`/`callback_data` value directly to it. Rubika's
`receiveInlineMessage` payload maps `aux_data.button_id` to `data`.
Rubika does not provide a callback-query ID, so `id=None` is intentional.

### Membership contracts

`IncomingChatMemberStatusUpdate` is only populated from Telegram's
`my_chat_member`/`chat_member` objects. `actor_id` is optional and is never
fabricated. Bale has `ChatMember` response models but no confirmed incoming
rich status-transition update; Rubika likewise has no such contract.

`IncomingBotMembershipChange` covers the simple bot-added/bot-removed
concept. Rubika maps explicit `EventData.BotJoined` and `EventData.BotRemoved`
to it. Rubika's event carries no confirmed actor ID, so `actor_id=None`.
Telegram/Bale message-level member lists remain on `IncomingMessage`; a
future dispatcher with known bot identity may derive a bot-membership change
from those fields rather than guessing inside the adapter.

`IncomingMessageDeleted` preserves Rubika `RemovedMessage` with its
`chat_id` and `removed_message_id`; it is not claimed to be a three-platform
common event.

### Payment contracts

`IncomingPreCheckoutQuery` is implemented for Telegram and Bale because
both platforms have confirmed top-level pre-checkout updates. Telegram's
`shipping_query` is represented by `IncomingShippingQuery` and is Telegram
only. `successful_payment` remains a field on `IncomingMessage`, matching
both Telegram and Bale model structure.

### PlatformCapabilities

The D1 capability regression values are:

| Capability | Telegram | Bale | Rubika |
|---|---:|---:|---:|
| `supports_topics` | true | false | false |
| `supports_scheduled_messages` | false | false | false |
| `update_delivery` | `both` | `both` | `both` |
| `supported_parse_modes` | Markdown, MarkdownV2, HTML | none confirmed | none confirmed |
| `callback_data_max_bytes` | 64 | 64 | none confirmed |
| `supports_payments` | true | true | false |
| `supports_admin_detection` | true | true | false |
| `supports_chat_member_status_updates` | true | false | false |

The Rubika `callback_data_max_bytes=None` value is deliberate: the audited
source establishes `button_id`, but does not establish a callback-data byte
limit. No unsupported limit is invented.

### D1 implementation boundary

The new package is `peyk.platform_core`, sibling to `peyk.platforms`. It
contains contracts and platform adapters only. No Router/Dispatcher,
Middleware, FSM, or formatting/keyboard-builder layer was added.

Each adapter also exposes `normalize_update()`. It normalizes every D0 event
for which a shared contract exists and returns the original platform update
unchanged for platform-specific event kinds, preserving the raw escape hatch
instead of dropping unsupported data.

## Dispatcher D2 — Router + filters decisions (2026-09-18)

D2 consumes only normalized `peyk.platform_core.contracts` objects. Raw
platform models are never passed to filters or registered handlers by the
router.

### Multi-match dispatch — superseded by Phase 5

D2 originally used dispatch-all semantics. Phase 5 supersedes this with
aiogram-compatible first-match-wins because the product API must not double-fire
a catch-all handler after a command handler. `SkipHandler` explicitly falls
through to the next candidate.

### Nested-router semantics

`include_router()` is structural composition. Child routers have independent
handler/filter registrations and do not inherit implicit filters from their
parent. This keeps inclusion from introducing hidden filtering context.

### Contract surface

D1 defines seven normalized event contracts that require router registration
methods: `IncomingMessage`, `IncomingCallbackQuery`,
`IncomingChatMemberStatusUpdate`, `IncomingBotMembershipChange`,
`IncomingMessageDeleted`, `IncomingPreCheckoutQuery`, and
`IncomingShippingQuery`. Simple message-level join/leave continues to be
filtered through `@router.message(...)` rather than becoming a separate
registration type.

### ChatType prerequisite

D2 requires a platform-agnostic `ChatType` filter, so `IncomingMessage` now
contains an explicit optional `chat_type` field. Telegram and Bale populate it
from their normalized message chat object. Rubika's audited message model does
not expose a confirmed chat type, so its adapter leaves the field `None`; the
filter consequently returns `False` instead of inspecting `.raw` or inventing
a value. This is a minimal contract completion required by the D2 acceptance
criteria, not a platform-specific shortcut.

`ChatType("group")` treats Telegram's `supergroup` as the canonical `group`
class while preserving `private` separately.


## Dispatcher D3 — Middleware decisions (2026-09-19)

### Single event-scoped middleware model

D3 deliberately uses one middleware concept rather than an aiogram-style
outer/inner pair. `Router.middleware(...)` registers an event-scoped wrapper
around that router's complete local dispatch subtree. This has the useful
property that middleware runs even when an event matches no handler, while
remaining sufficient for cross-cutting concerns such as logging, permission
gates, and dependency/context injection. Middleware is not attached to raw
platform objects.

A registered middleware chain is ordered outward-in by registration order:
`m1 -> m2 -> dispatch -> m2 -> m1`. A middleware may choose not to call its
`handler` continuation to short-circuit dispatch (for example, a permission
gate). The mutable `data` dictionary belongs to one `propagate_event()` call
and is passed through the middleware chain to matching handlers. Handlers
receive only context keys accepted by their signature, unless they declare
`**kwargs`, in which case all injected context is passed. Existing event-only
handlers therefore remain source-compatible.

Included routers are structural subtrees. A parent router's middleware wraps
its entire subtree; a child router's own middleware wraps that child subtree
when reached. Middleware registration is independent per router.

### Middleware exception isolation — extended by Phase 5

Phase 5 extends D3 with aiogram-style observer inner/outer middleware while
retaining `Router.middleware(...)` as the outer whole-subtree middleware.
Handler exceptions now terminate the current propagation candidate and are sent
to `router.errors`; they do not invoke later sibling handlers. Middleware
exceptions follow the same error-observer path. This change is required for
first-match-wins and aiogram parity.

### Logging integration

`LoggingMiddleware` uses the existing transport logging-hook abstraction rather
than introducing a separate logging configuration. The existing
`TransportLogger`/`StdlibTransportLogger` hook gains an additive `log_event`
operation. Events are logged by normalized contract type only; the middleware
does not inspect `.raw`. A compatibility fallback remains for custom logger
objects that predate `log_event`.


## Dispatcher D4 — FSM + storage decisions (2026-09-19)

D4 adds a declarative `State`/`StatesGroup` API, `FSMContext`, asynchronous
storage protocol/backends, and `StateFilter` without moving platform parsing
into the dispatcher. FSM conversation identity is keyed by chat/user identity
plus a platform namespace. For normalized Telegram/Bale/Rubika events, that
namespace is inferred from the raw model module only for collision isolation;
the router and filters continue to consume normalized contracts.

`MemoryStorage` is deliberately ephemeral. An unfinished conversation can be
re-triggered after a process restart, so losing that state is a genuinely safe
loss under the project's anti-speculative-caching rule. This does not imply
that ownership or security state should use the same backend.

Redis is optional and exposed as `peyk[fsm-redis]`; the base installation does
not pull in a Redis client. The Redis implementation stores state separately
from JSON-encoded conversation data and can use an externally supplied async
Redis client, which also keeps tests free of a real Redis server.

## Dispatcher D5 — formatting + keyboard builder decisions (2026-09-19)

### Rich text

`RichText` is an immutable intermediate representation. Rendering is selected
from confirmed `PlatformCapabilities.supported_parse_modes`; no raw platform
markup is stored in the public builder API. Telegram prefers HTML, then
MarkdownV2, then legacy Markdown. When no parse mode is advertised, formatting
is stripped rather than leaking markup.

The supplied Bale audit does not establish a parse mode, so Bale capabilities
remain empty and D5 deliberately does not assume Telegram-compatible parsing.
The supplied Rubika source confirms formatting through `sendMessage.metadata`
(`MetadataPart.type`, offsets, length, and `link_url`) rather than a parse-mode
field. Therefore `render_for()` uses plain text for Rubika, and the separate
`render_rubika_metadata()` helper emits the confirmed structured form.

### Keyboard builder

`KeyboardBuilder` targets a common inline-button subset for Telegram/Bale and
Rubika. Platform-specific Rubika controls (`Calendar`, `NumberPicker`) are
explicit and raise `KeyboardBuildError` when another platform is selected.
Callback data is checked when `build()` is called using the target's
capability limit. Telegram and Bale are confirmed at 1–64 UTF-8 bytes. Rubika
continues to advertise `callback_data_max_bytes=None` because the earlier audit
explicitly found no confirmed byte limit; no unsupported limit is invented.

## Dispatcher D5 formatting/keyboard clarification (2026-09-19)

The original D5 implementation is refined to distinguish **parse_mode** from a
platform's native text syntax. Telegram continues to use its advertised parse
modes. Bale is treated as having no Telegram-style `parse_mode`; its renderer
emits the project's confirmed Bale syntax directly: `*bold*`, `_italic_`,
`[text](url)`, `[text](uid:user_id)`, `[text](ble.ir/username)`, triple-backtick
code/pre blocks, and `[title]```content```` for the copy-friendly expanded
view. Unsupported Bale formatting nodes are stripped instead of leaking raw
markup.

Rubika's public bot documentation/research found structured `Metadata` support
rather than a Telegram-like `parse_mode`; third-party API documentation also
shows Bold/Italic/Mono/Underline/Strike/Spoiler/Link-style metadata. The
project therefore keeps `render_rubika_metadata()` as an explicit opt-in
adapter helper, while the normal `render_for(..., RUBIKA_CAPABILITIES)` path
sends plain text as required by the cross-platform contract. No Rubika
parse-mode string is advertised.

The keyboard builder now exposes every button discriminator represented by the
current Rubika model: Selection, Calendar, NumberPicker, StringPicker,
Location, CameraImage, CameraVideo, GalleryImage, GalleryVideo, File, Audio,
RecordAudio, Textbox, Link, AskMyPhoneNumber, AskMyLocation, and Barcode.
Rubika-only types fail loudly on Telegram/Bale. Bale/Telegram also expose
reply-keyboard contact/location convenience buttons. The common `button()` and
`url()` API remains unchanged.

## Refactor R0 — aiogram-3-style public API

**Status: accepted** (2026-09-19). This phase documents the design decisions for
the aiogram-3-style public API surface; each decision notes the later phase
that implements it.

### 1. Public import layout

```python
from peyk import Bot, BaleBot, TelegramBot, RubikaBot, Dispatcher, Router, F
import peyk.filters
import peyk.types
import peyk.keyboard
import peyk.enums
import peyk.fsm
```

Old import paths remain as re-export shims; deprecated paths emit
`DeprecationWarning`.

- **Implemented in:** Phase 1 (public `__init__.py` surface), Phase 2
  (`filters`, `types`, `enums`, `keyboard` packages), Phase 3 (`fsm` package).

### 2. Router dispatch semantics — first-match-wins

`Router.propagate_event()` switches from D2's dispatch-all to
**first-match-wins**: the first handler whose filter matches is invoked and
the router stops. A `SkipHandler` exception lets a matching handler opt out
and fall through to the next candidate. This supersedes D2's dispatch-all
rule.

Router-level filters remain via `router.message.filter(...)`. D3's single
outer middleware model stays as the "outer" middleware layer; no inner
middleware is introduced.

- **Implemented in:** Phase 5.

### 3. Platform selection

Two API levels:

1. **Simple:** `Bot(token, platform="bale" | "telegram" | "rubika")` plus
   `BaleBot`/`TelegramBot`/`RubikaBot` shortcut subclasses.
2. **Aiogram-style:** explicit `Bot`/`Dispatcher`/`Router` composition.

`bot.client` exposes the raw platform client, **typed per subclass**
(`BaleClient` for `BaleBot`, `TelegramClient` for `TelegramBot`, `RubikaClient`
for `RubikaBot`). User code never passes a platform name around — the platform
is selected at `Bot` construction and concrete types flow from there.

- **Implemented in:** Phase 4 (Bot/Dispatcher/Router shells), Phase 6 (typed
  client subclasses).

### 4. `F` comes from `magic-filter`

The `F` object is imported from the `magic-filter` package, giving aiogram
users the identical syntax (`F.text`, `F.command`, `F.from_user.id == 5`,
`F.text.startswith("/")`). `magic-filter` becomes a normal runtime dependency.

- **Implemented in:** Phase 2.

### 5. Unsupported-feature policy

- **Cosmetic features** (button color, formatting, callback toast) **degrade
  by default** — the bot continues to function, just without the cosmetic
  nuance.
- **Functional features** raise `UnsupportedFeatureError` — the user code path
  genuinely cannot work on the active platform.
- Overridable via `Bot(on_unsupported=...)` callback to customize the policy.

- **Implemented in:** Phase 4 (exception class + `Bot` hook), applied across
  all platforms as features land.

### 6. Three-state capability values

Capability values are **three-state**: `yes`, `no`, or `UNKNOWN` (Python
`None`). Anything not confirmed by audited code, platform documentation, or
`docs/decisions.md` is `UNKNOWN` — never `yes`, never `no`, never a fabricated
limit.

The `PlatformCapabilities` dataclass already uses `Optional[int]` for
`callback_data_max_bytes` (Rubika: `None` = UNKNOWN) and `bool` for
boolean capabilities (confirmed `true`/`false`). No change to existing
booleans; `UNKNOWN` applies only to numeric/string capabilities where the
audit found no authoritative source.

- **Implemented in:** Phase 4 (capability enforcement in `Bot` and builders).

## Capability R1 — real capability matrix and audit (2026-09-19)

**Status: accepted.** Phase 1 introduces a declarative, machine-audited
capability registry under `peyk.platform_core.capabilities`.

1. `Feature` is a stable cross-platform vocabulary grouped by messaging,
   keyboards, callbacks, updates, chat administration, files, payments,
   bot-profile/inline mode, and Telegram-only surfaces.
2. `SupportLevel` distinguishes `FULL`, `PARTIAL`, `EMULATED`, `NONE`, and
   `UNKNOWN`; the registry never converts missing evidence into support.
3. Each support record carries evidence, limits, notes, and confidence. Method
   evidence is resolved through class MRO, while model evidence uses
   `dataclasses.fields`.
4. The old nine-field `PlatformCapabilities` objects remain compatibility
   projections derived from the registry; their D1 values are regression
   tested unchanged.
5. The capability audit is generated and checked by
   `scripts/audit_capabilities.py`. Every public coroutine and keyboard-button
   field is either represented by a cross-platform feature or explicitly
   classified as platform-specific. Generated matrix and TODO documentation
   are committed.
6. `UnsupportedFeatureError` is defined now as the common error type for the
   capability enforcement work planned for Phase 2; Phase 1 does not invoke
   it from clients.

## Refactor R5 — aiogram-3 Router semantics + filters (2026-09-19)

**Status: accepted.** The maintainer's `D:\aiogram` source was not accessible
in this environment, so the implementation follows the explicit Phase 5 rules
and is marked **unverified vs aiogram** where direct source comparison was
required. No behavior is claimed from inaccessible source.

### Router semantics

Observers are first-class objects with decorator, `register`, observer-level
`filter`, inner `middleware`, and outer `outer_middleware` APIs. `Router.middleware`
remains the D3 outer whole-subtree layer. Handler propagation is
first-match-wins, with `SkipHandler` providing explicit fall-through.
Included routers are traversed in inclusion order after the current router's
own handlers. Handler/middleware failures are delivered to `router.errors` as
`ErrorEvent`; an unhandled error is logged and does not terminate polling.

### Filters

The public filter package is `peyk.filters`; `peyk.dispatcher.filters` remains
a deprecated re-export shim. `F` is the `magic-filter` root `MagicFilter`.
Filter results may contribute dependency-injection data through dictionaries.
Legacy event-only filters remain adaptable by signature inspection.

`CallbackData` is dataclass-based and does not add pydantic. Packing is
platform-agnostic; audited byte limits remain a keyboard-render concern for
Phase 6.

### Compatibility and intentional differences

The explicit Phase 5 rules take precedence over the previous D2/D3 decisions:
first-match replaces dispatch-all, observer middleware gains an inner layer,
and filter execution may merge dictionaries into handler data. These are
intentional product requirements, not accidental compatibility changes.
The previous old-path imports remain available with `DeprecationWarning`.

- **Implemented in:** Phase 5.
- **Aiogram source comparison:** unverified because `D:\aiogram` was not
  available to this environment.

## Refactor R2 — Bot + neutral bound objects (2026-09-19)

**Status: accepted.** Phase 2 adds the neutral event/action layer and the
platform-neutral `Bot` facade without changing dispatcher, polling, or keyboard
IR behavior.

1. `peyk.types` owns neutral `User`, `Chat`, `Message`, `CallbackQuery`, and
   related neutral value types. `Message` subclasses the existing
   `IncomingMessage` contract so current dispatcher/filter `isinstance`
   checks remain valid. The platform model remains available through `.raw`.
2. Chat types normalize Telegram `supergroup` to `group`; unknown source chat
   kinds remain `unknown` rather than being guessed.
3. Normalized inbound events are initially unbound. `Bot.normalize_update()`
   binds supported `Message`/`CallbackQuery` objects to the creating bot, and
   event actions raise `BotNotBoundError` when no bot is attached.
4. Bot operations use one strategy module per platform rather than adding a
   platform branch to every public operation. Rubika media uses the already
   audited `requestSendFile` -> upload -> `sendFile` flow; no new Rubika media
   capability is assumed.
5. Unsupported behavior is decided from the Phase 1 capability registry. The
   default policy raises for functional gaps and degrades cosmetic gaps with a
   once-per-platform/feature warning. No platform-name condition is used to
   decide support.
6. `KeyboardBuilder` accepts the audited capability set as the Phase 6
   `_resolve_markup` seam; it does not introduce a new keyboard IR in this
   phase.

**Deferred:** `Dispatcher`, automatic polling, first-match routing, `F`, and
new keyboard IR remain later phases.

## Refactor R3 — Dispatcher + automatic polling (2026-09-19)

**Status: accepted.**

1. `Dispatcher` subclasses `Router` and remains the root event entry point. It
   owns workflow data and injects `bot`, `dispatcher`, `event_from_user` and
   `event_chat` before propagation. Router matching semantics are unchanged;
   first-match dispatch remains a later phase.
2. Polling is represented by a small `Poller` protocol with one concrete
   poller per platform. Telegram and Bale own numeric `update_id` offsets;
   Rubika owns the documented string `next_offset_id`. Rubika
   `updateBotEndpoints` is not called implicitly because its endpoint
   parameter semantics remain low-confidence.
3. Telegram/Bale webhooks are cleared before polling when necessary. When
   `skip_updates=True`, Telegram uses `drop_pending_updates=True`; Bale uses
   its audited parameterless `delete_webhook`. Existing webhooks are removed
   before polling even when pending updates are retained, because polling
   must not silently coexist with a configured webhook.
4. Polling errors use the existing transport `RateLimitedError` retry hint and
   exponential backoff with jitter for network/timeout/unexpected failures.
   Authentication/authorization failures stop only the affected bot instead
   of retrying forever.
5. Updates are handled sequentially by default to preserve per-chat ordering
   for future FSM use. `handle_as_tasks=True` opts into concurrent handler
   tasks bounded by `max_concurrent_updates`; shutdown awaits pending handler
   tasks.
6. Signal installation is best-effort. `NotImplementedError` and
   `RuntimeError` from `loop.add_signal_handler` are treated as the Windows /
   embedded-loop fallback, while normal cancellation and `KeyboardInterrupt`
   still unwind through the polling cleanup path.
7. Startup and shutdown observers are router-local and are emitted
   recursively from the dispatcher root through included routers. This adds
   lifecycle hooks without changing event matching.

Later implementation phases: Router first-match semantics and `SkipHandler`
remain Phase 5; FSM wiring remains its planned phase; webhook mode is not part
of R3.


## Refactor R4 — simple Bot API (2026-09-19)

**Status: accepted.**

The simple public entry point is `Bot(token, platform=...)` with a plain
`bot.router`. Decorators register handlers on that router and return the
original callable unchanged, preserving IDE signatures and allowing the same
router to be included later in an explicit `Dispatcher`. This is implemented
in Phase 4.

`bot.run()` is a blocking wrapper around `bot.run_async()`, which creates an
explicit dispatcher, includes `bot.router`, validates the bot identity before
polling, and then delegates automatic polling to the Phase 3 dispatcher. The
module-level `peyk.run(*bots)` uses one asyncio loop and runs each bot's
independent router concurrently. This is implemented in Phase 4.

Startup and shutdown decorators are bare-decorator forms backed by the
existing Router lifecycle observers. No Router matching behavior is changed;
first-match semantics remain a later phase.

Command aliases are registered as separate `Command` filters so aliases do
not require an OR filter abstraction. Callback registration reuses the
existing callback-data equality/prefix filters. The `prefix` argument is part
of `Command` so non-slash command prefixes remain explicit rather than being
rewritten by the simple API.

A bot created outside an active asyncio loop delays construction of its raw
HTTP client until first use. This is required so the documented blocking
`Bot(...); bot.run()` form does not bind an aiohttp session to the wrong loop.

Invalid authentication during the pre-polling `me()` check is normalized to
`InvalidTokenError`; no platform-specific token error is inferred beyond the
audited HTTP 401/403 response shape.

## Refactor R6 — platform-neutral keyboard IR and render-at-send (2026-09-19)

**Status: accepted.** Phase 6 moves keyboard construction to a neutral IR and
selects a native representation only when a Bot sends the markup.

1. `peyk.keyboard` owns frozen neutral button/keyboard dataclasses and the
   aiogram-compatible builders. The old `peyk.utils.KeyboardBuilder` remains a
   compatibility shim and continues to support `.build(target)` while warning
   that the API is deprecated.
2. `InlineKeyboardBuilder` and `ReplyKeyboardBuilder` enforce the audited
   aiogram limits of eight buttons per row and 100 buttons total. `adjust()`
   operates on the flattened button sequence; `row()` chunks at the requested
   width.
3. Renderers are pure platform-specific functions. Telegram/Bale native model
   fields are copied only when the audited model actually contains them.
   Rubika inline markup is rendered as `inline_keypad`; reply markup uses
   `chat_keypad` with `chat_keypad_type="New"`, and removal uses `"Remove"`.
4. Callback data is packed at render time. Telegram/Bale enforce their audited
   64-byte UTF-8 limit; Rubika remains unchecked because its callback-data byte
   limit is still UNKNOWN/low-confidence.
5. Functional unsupported fields raise `UnsupportedFeatureError` unless a
   button supplies a fallback. Cosmetic style/icon gaps degrade by default.
   `BotDefaults.style_fallback=StyleFallback.EMOJI` may add a colored emoji
   prefix when native button style is unavailable. Telegram is the only
   platform currently audited as having a native `style` field; the exact
   `primary`/`success`/`danger` wire values are marked **inferred** because the
   repository confirms the field but not those value strings.
6. User code does not name a platform. `Bot._resolve_markup()` is the single
   integration seam: neutral IR/builders are rendered against the Bot's
   capability set at send time; already-native objects remain an explicit raw
   escape hatch.

Aiogram source comparison remains **unverified** because `D:\aiogram` was not
available in this environment. The implementation follows the explicit Phase 6
rules and the repository's audited native models.


## Refactor R7 — formatting composition and send-time resolution (2026-09-19)

Phase 7 adds an aiogram-style formatting composition layer without replacing
the existing RichText intermediate representation or its renderers. `Text` and
the formatting node classes compile into the existing IR; rendering is delayed
until the active bot operation knows its platform.

`str` content remains literal text. `BotDefaults.parse_mode` is applied to
plain strings, while `RichText`/`Text` uses the audited renderer selection:
Telegram HTML, Bale native project syntax, and Rubika plain text plus explicit
metadata on operations whose client accepts that metadata.

Explicit `parse_mode` is represented by the neutral `ParseMode` enum (plain
strings remain accepted for compatibility). Telegram forwards a supported
explicit mode. Bale and Rubika have no confirmed parse-mode request field, so
DEGRADE/STRIP sends unparsed text with one warning per `(platform, feature)`;
RAISE raises `UnsupportedFeatureError`. No arbitrary markup string is
auto-converted.

Rubika `edit_message_text` has no metadata parameter. A formatted edit
therefore degrades to plain text with a once-only warning, or raises under
RAISE. Rubika media-caption metadata is likewise not forwarded unless a client
signature confirms such a parameter.

Rubika metadata offsets currently use Python string positions (Unicode code
points). The protocol unit is UNCONFIRMED; this choice is isolated in
`RUBIKA_METADATA_OFFSET_UNIT = "codepoint"` and covered by a Persian+emoji
regression test.

Bale has no confirmed escaping rule for its native inline syntax in the
audited project. We do not invent an escape convention. Existing native
rendering is retained and this remains LOW-confidence; applications should
avoid treating untrusted Bale markup as a security boundary until a live or
official syntax rule is established.

`peyk.utils.html` and `peyk.utils.markdown` are intentionally Telegram syntax
helpers and are not portable formatting abstractions.

## Dispatcher D6 — FSM integration, migration, and Phase 8 (2026-09-19)

**Status: implemented for checkpoints A+B; checkpoint C intentionally stopped.**

### A — FSM core

1. `StorageKey` is a frozen dataclass with `(platform, bot_id, chat_id,
   user_id, destiny="default")`. Telegram/Bale integer IDs and Rubika string
   IDs are preserved as `int | str`. A `thread_id` field was **not** added:
   the neutral `IncomingMessage`/`Message` contract in this repository exposes
   no topic/thread identifier, so adding one would invent a cross-platform
   capability.
2. `DefaultKeyBuilder` follows the aiogram key-builder shape but always puts
   `platform` in the namespace and defaults `with_bot_id=True`. The bot token
   is never part of a key. State/data/lock are separate key parts.
3. `BaseStorage`, `MemoryStorage`, and `RedisStorage` now operate on
   `StorageKey`. String keys remain only as a deprecated compatibility path so
   the pre-Phase-8 tests and user code can migrate incrementally. FSM data is
   typed as `dict[str, object]` in new public APIs rather than adding `Any` to
   new signatures.
4. Redis supports independent `state_ttl` and `data_ttl` values and keeps the
   Redis client optional behind `peyk[fsm-redis]`. The implementation accepts
   an injected async Redis client, which keeps tests offline.
5. `BaseEventIsolation` provides `lock(key)`. `DisabledEventIsolation` is a
   no-op; `SimpleEventIsolation` keeps one `asyncio.Lock` per key and removes
   idle entries; `RedisEventIsolation` uses a Redis distributed lock.
6. `FSMStrategy.USER_IN_CHAT` is the default. `CHAT` and `GLOBAL_USER` are
   supported. Topic variants are deliberately absent because `thread_id` is
   not present in the neutral contract.
7. `FSMContext(storage, key)` is the new canonical constructor. The previous
   `FSMContext(event, storage, platform=...)` form remains through a deprecated
   compatibility path, and `FSMContext.for_event(...)` is the explicit event
   adapter. New dispatcher code never guesses a platform from a raw model.
8. `State` accepts `state=None` and `group_name=None`, supports wildcard
   `any_state`, and `StatesGroup` exposes direct/nested state metadata including
   `__states__`, `__state_names__`, `__all_states__`, and the corresponding
   nested metadata used by the filter. `default_state` matches an empty FSM
   state and `any_state` matches every state.
9. `StateFilter` reads `raw_state` from dependency-injection data and supports
   `State`, `StatesGroup`, `str`, `None`, regular expressions, `default_state`,
   and `any_state`. Its explicit-storage constructor is deprecated but retained
   for migration.

### B — Dispatcher integration

1. `Dispatcher` now defaults to `MemoryStorage`, `USER_IN_CHAT`, and
   `SimpleEventIsolation`. `FSMContextMiddleware` is registered as the
   dispatcher's outer whole-subtree middleware and injects `state` and
   `raw_state` into handlers.
2. The middleware builds every key from `bot.platform` + authenticated
   `bot.id` + the normalized event identity. The dispatcher fetches `bot.me()`
   before polling and before processing an event, so a missing bot ID fails
   clearly instead of producing an ambiguous FSM namespace.
3. Isolation covers the complete handler execution, including async handlers
   launched by `handle_as_tasks=True`. Different storage keys do not share the
   same in-process lock.
4. Rubika `receiveInlineMessage` is normalized through the existing neutral
   `IncomingCallbackQuery` shape. Its `aux_data.button_id` and sender/chat
   identity therefore use the same FSM key as an ordinary message.
5. `scripts/bot.py` is now a single `Router` + `Dispatcher` + FSM example;
   manual storage, state lookup, platform-specific handler branches, and the
   hand-written polling loop were removed. `examples/finite_state_machine.py`
   demonstrates the same registration flow across all configured platforms.

### Known compatibility differences from aiogram 3

The local reference requested by Phase 8 (`D:\\aiogram`) was not mounted or
readable in this environment, so the source-dependent Scenes checkpoint was
not implemented. The core API follows the publicly visible aiogram 3 state
model, but Peyk intentionally differs where its multi-platform contract
requires it: platform is always in the key, bot ID is on by default, IDs are
`int | str`, topic strategies are omitted without a neutral thread field, and
legacy Peyk constructors/storage string keys remain available through
DeprecationWarnings. Peyk's public new FSM data signatures use `object` values
instead of adding `Any`.

### Checkpoint C — Scenes

**Not implemented.** The requested local aiogram source tree was unavailable,
so `Scene`, `SceneRegistry`, `ScenesManager`, `SceneWizard`, scene-as-router,
`After.goto/exit/back`, and the scene tests/examples were intentionally left
out rather than guessed. This is a Phase 8 open item, not a claimed absence of
those capabilities in aiogram.

## Webhook W1 — framework-agnostic processing and security (2026-09-19)

Phase 9 adds a server-independent `WebhookProcessor`. It verifies the
Telegram secret header when configured, enforces a maximum body size, parses
only repository-confirmed platform models, and feeds the resulting raw update
to the existing `Dispatcher.feed_raw_update` path. Successful deliveries are
acknowledged with HTTP 200 immediately by default while tracked background
handler tasks finish during webhook shutdown. Malformed JSON is HTTP 400 and
oversized bodies are HTTP 413. Authentication/path failures are intentionally
HTTP 404 to avoid a secret oracle.

Every webhook URL contains a random path secret by default. Applications that
register a URL externally should supply a stable secret so the URL remains
stable across restarts. Telegram additionally receives that secret as
`secret_token`, which is enforced through `X-Telegram-Bot-Api-Secret-Token`.
Bale and Rubika have no confirmed platform secret/header mechanism; their
webhook protection therefore relies on the Peyk path secret, with IP filtering
available as an explicit server-side control. Unsupported platform-specific
secret-header options raise `UnsupportedFeatureError` instead of being
silently ignored.

`constant_time_compare` moved to `peyk.webhook.security`; the former Rubika
module remains a deprecation shim. `IPFilter` defaults to the transport peer
address; `X-Forwarded-For` is used only when `trust_forwarded_for=True`.
Telegram's official network list is shipped as an opt-in constant and is not
a default allow-list.

## Webhook W2 — platform registrars and unified automation (2026-09-19)

Telegram registration uses `set_webhook` with `secret_token`,
`allowed_updates`, `drop_pending_updates`, and `max_connections`. Bale uses
only its confirmed `set_webhook(url)` contract. Rubika registers only
`ReceiveUpdate` and `ReceiveInlineMessage`, with the latter at an `/inline`
sub-path; `GetSelectionItem` and `SearchSelectionItems` are deliberately not
implemented until their dynamic response bodies are evidenced.

`Dispatcher.start_webhook`/`run_webhook` builds one aiohttp application for a
mixed list of Telegram, Bale and Rubika bots. URL routing uses
`{platform}/{secret}` and never uses the bot token. Startup fetches each
`bot.me()` and installs registrations; shutdown waits for background webhook
tasks, optionally removes registrations, closes bots, and lets aiohttp execute
registered shutdown hooks. `asyncio.run` is used by `run_webhook`, including on
Windows where POSIX signal handlers are unavailable.

The unified `Bot.set_webhook`, `delete_webhook`, and `get_webhook_info` facade
checks the audited capability matrix before calling platform clients. Rubika
has no confirmed `getWebhookInfo`/delete operation in the audited contract, so
its unified read/remove operations are not claimed as supported.

The Telegram client's audited `set_webhook` signature has no `certificate`
parameter, so self-signed certificate upload remains out of scope for this
phase. Webhook responses do not contain handler replies; replying inside the
HTTP response is also out of scope.


## Phase 10A — enums and native event observers (2026-09-19)

Phase 10A exposes the small finite domains used by the neutral dispatcher
from ``peyk.enums`` and keeps Telegram-only Bot API discriminators under
``peyk.platforms.telegram.enums``. ``ButtonStyle`` is the Phase 6 enum and is
re-exported rather than duplicated. Existing ``peyk.types.ChatType`` and
``ContentType`` now refer to the same neutral enum definitions. Rubika's
existing constant classes are intentionally unchanged: converting them to
``Enum`` would alter their established class/type surface without evidence
that downstream code expects enum semantics, so that migration is deferred.

The local ``D:\\aiogram`` source/YAML reference was not readable in this
environment. Phase 10A therefore used the repository's audited Telegram model
surface and the current official Bot API documentation for the enum wire
values. The generated YAML comparison remains an open verification item.
Where the Bot API documents an open ISO-4217 currency domain, ``Currency``
currently exposes only the repository/API-confirmed ``XTR`` member rather
than inventing a closed currency list.

Router dispatch now has a framework-agnostic ``platform_event`` observer. It
receives the complete native update object and always has ``bot`` in DI.
Telegram also gets named native observers for every field present in the
repository's ``Telegram.Update`` model, including ``inline_query`` and
``chat_join_request``. ``InlineQuery.answer`` and
``ChatJoinRequest.approve/decline`` are thin bound helpers over existing
Telegram client methods.

Neutral message routing now distinguishes ``message``, ``edited_message``,
``channel_post`` and ``edited_channel_post`` using an explicit
``Message.update_kind``. ``router.message`` therefore handles only new
non-channel messages, matching aiogram's observer separation. Telegram's
channel/business fields are routed from their native Update fields; Bale and
Rubika are only assigned kinds evidenced by their local models (Rubika
``UpdatedMessage`` becomes ``edited_message``).

When Telegram-native observers are registered for a Bale or Rubika dispatcher,
startup emits one warning naming the unsupported observers instead of silently
claiming that those platforms deliver them.

## Phase 10B — aiogram utility parity (2026-09-19)
- Handler flags are stored on the registered handler record and injected as `handler`/`flags`, so middleware sees the exact registration-time values.
- Chat-action and callback-answer middleware are capability-gated; no unsupported platform call is synthesized. Rubika receives no chat-action/callback-answer request where the audited matrix does not establish support.
- Deep links are implemented only for Telegram because its `t.me/<username>?start=` format is confirmed. Bale/Rubika formats remain UNKNOWN rather than guessed.
- Web App init-data validation is Telegram-only; no Bale equivalent was found in the audited contract.
- Media groups use the existing Telegram/Bale client methods. Rubika is not claimed to support them without matrix evidence.
- i18n uses the standard-library GNU gettext loader, with locale selection supplied by DI middleware.

## Phase 10C — typing sweep and documentation (2026-09-19)

- The supplied Telegram Butcher schema is API version 10.2 (2026-07-14). Method-name verification found all 185 schema methods represented either by Telegram method modules or the shared Telegram-like base; no schema method is missing from the effective client surface. Two local public helpers (`build_inline_keyboard_button`, `close_bot`) are outside the Bot API schema and are retained because they are peyk compatibility/helpers, not Telegram Bot API methods.
- The supplied method schema does not contain a structured `returning` field. Return annotations are therefore derived only from explicit documented return prose, with explicit union/list cases recorded in `sync_telegram_from_schema.py`; no undocumented return type was guessed.
- Telegram type field structures were verified before documentation changes. 138 concrete class field sets differ from the supplied schema; these are reported and intentionally not auto-fixed because changing fields would be a runtime/API compatibility change outside this typing/docstring phase.
- Telegram method docstrings now use schema summaries and parameter descriptions. Telegram model class docstrings expose schema field descriptions through an `Attributes` section.
- Bale and Rubika/shared public surfaces received substantive docstrings. Bale documents `close_bot` and `getChatMembersCount`; Rubika documents wrapped responses, the three-step upload flow, and `offset_id`. Main Bot/RichText entry points include examples.
- Public `Any` annotations are now zero under `scripts/audit_any.py`; the allow-list is intentionally empty. `py.typed` is shipped and strict mypy is configured globally. The environment does not contain mypy, so strict mypy execution remains unverified.
- Sphinx `autodoc_typehints` is set to `signature`; `sphinx-build -W` could not be executed because Sphinx is not installed in the environment.
- Placeholder-producing docstring generator scripts were deleted. `scripts/audit_docstrings.py` is a testable gate for missing public docs, placeholder patterns, and undocumented `Args` entries.


## Phase 10D — documentation, logo, examples, release (2026-09-19)

- The documentation site now uses the repository logo as a real static asset,
  with optimized light/dark variants and 32/64px favicons. The original image
  is retained unchanged under `assets/logo-source.png` so documentation builds
  do not depend on a generated derivative.
- The guide order starts with the simple `Bot(...).run()` path and then moves
  to explicit Dispatcher/Router usage. This mirrors the product goal rather
  than presenting internal architecture first.
- Platform capability documentation embeds the audited generated matrix instead
  of restating feature support from memory. UNKNOWN entries remain UNKNOWN.
- The migration guide documents the deliberate differences from aiogram: the
  one-time `platform` selection, neutral objects, `.raw`, `bot.client`, and
  capability-aware degradation/raising.
- Examples use only public imports and keep network execution behind
  `if __name__ == "__main__"` so import checks are offline.
- Release metadata is set to 0.2.0. The release notes record the known
  compatibility changes rather than claiming full aiogram wire-level identity.
- A separate Scene API is not documented as an existing public feature; the FSM
  guide describes state-group-based scene-style flows because that is the
  implemented public surface.


## Docs theme refresh (2026-09-20)

- The sidebar showed two large logos because `html_logo` and Furo's
  `light_logo`/`dark_logo` are rendered together. Only `html_logo` is set now.
- The logo is shipped as a transparent SVG (`docs/_static/logo.svg`,
  `docs/_static/favicon.svg`, `assets/logo.svg`), vectorised from
  `assets/logo-source.png`, which is kept unchanged as the source.
- The landing page no longer embeds a large image; a small logo sits next to the
  title via CSS (`.. rst-class:: peyk-home` in `index.rst`).
- Look and feel: blue->cyan palette taken from the logo, navy dark mode, rounded
  corners, card-style toctrees on the landing page. Colours live in
  `html_theme_options` (`light_css_variables` / `dark_css_variables`), layout in
  `_static/custom.css`. Pygments styles were intentionally left at Furo defaults.
- Not verified here: `sphinx-build` (Sphinx/Furo were not installed).
