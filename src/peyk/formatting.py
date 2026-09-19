"""aiogram-style composable formatting built on Peyk's RichText IR.

The composition objects are platform-neutral. Rendering happens only when a
target platform is known, so application code does not carry platform names.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Protocol, Sequence, Union, cast
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from peyk.bot.policy import UnsupportedPolicy
from peyk.platform_core.contracts import PlatformCapabilities
from peyk.platform_core.enums import ParseMode
from peyk.platform_core.errors import UnsupportedFeatureError
from peyk.utils.text_formatting import RichText, _Element, _Text, bale_expandable, bold, code, italic, link, mention_user, mention_username, pre, render_for, render_rubika_metadata, spoiler, strikethrough, underline
Content = Union[str, RichText, 'Text']

class TextDefaults(Protocol):
    """Minimal defaults contract required by :func:`resolve_text`."""
    parse_mode: ParseMode | str | None

def _rich(value: Content) -> RichText:
    if isinstance(value, Text):
        return value.to_rich_text()
    return RichText.from_value(value)

@dataclass(frozen=True)
class Text:
    """A composable sequence of text fragments and formatting nodes."""
    body: tuple[Content, ...]

    def __init__(self, *body: Content, sep: str='') -> None:
        if sep:
            parts: list[Content] = []
            for index, item in enumerate(body):
                if index:
                    parts.append(sep)
                parts.append(item)
            body = tuple(parts)
        object.__setattr__(self, 'body', tuple(body))

    def to_rich_text(self) -> RichText:
        """Compile this composition into Peyk's platform-neutral IR."""
        result = RichText()
        for item in self.body:
            result = result + _rich(item)
        return result

    def __add__(self, other: Content) -> 'Text':
        """Return a new composition containing ``other``."""
        return Text(*self.body, other)

    def render(self, target: PlatformCapabilities | str) -> str:
        """Render this composition for a platform or audited capability object."""
        return render_for(self.to_rich_text(), _target_capabilities(target))

    def as_kwargs(self, target: PlatformCapabilities | str) -> dict[str, object]:
        """Return the exact text-bearing keyword arguments for ``target``."""
        caps = _target_capabilities(target)
        if caps.platform == 'rubika':
            text, metadata = render_rubika_metadata(self.to_rich_text())
            return {'text': text, 'metadata': {'meta_data_parts': metadata}}
        text = render_for(self.to_rich_text(), caps)
        if caps.platform == 'telegram':
            return {'text': text, 'parse_mode': 'HTML'}
        return {'text': text}

class Bold(Text):
    """Render children in bold."""

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return bold(_compile_body(self.body))

class Italic(Text):
    """Render children in italics."""

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return italic(_compile_body(self.body))

class Underline(Text):
    """Render children with an underline where the target supports it."""

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return underline(_compile_body(self.body))

class Strikethrough(Text):
    """Render children with a strikethrough where the target supports it."""

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return strikethrough(_compile_body(self.body))

class Spoiler(Text):
    """Render children as a spoiler where the target supports it."""

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return spoiler(_compile_body(self.body))

class Code(Text):
    """Render children as inline code."""

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return code(_compile_body(self.body))

class Pre(Text):
    """Render children as a preformatted block."""

    def __init__(self, *body: Content, language: str | None=None) -> None:
        super().__init__(*body)
        object.__setattr__(self, 'language', language)
    language: str | None

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return pre(_compile_body(self.body), self.language)

class TextLink(Text):
    """Render children as a URL link."""

    def __init__(self, *body: Content, url: str) -> None:
        super().__init__(*body)
        object.__setattr__(self, 'url', url)
    url: str

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return link(_compile_body(self.body), self.url)

class TextMention(Text):
    """Render children as a Telegram user mention."""

    def __init__(self, *body: Content, user_id: int | str) -> None:
        super().__init__(*body)
        object.__setattr__(self, 'user_id', user_id)
    user_id: int | str

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return mention_user(_compile_body(self.body), self.user_id)

class BlockQuote(Text):
    """Render children as a block quote."""

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return _wrap_composition('blockquote', self.body)

class ExpandableBlockQuote(Text):
    """Render children as an expandable block quote."""

    def to_rich_text(self) -> RichText:
        """Provides the to rich text operation for the peyk integration.

Returns:
    Result produced by the operation."""
        return _wrap_composition('expandable_blockquote', self.body)

def _compile_body(body: Sequence[Content]) -> RichText:
    result = RichText()
    for item in body:
        result = result + _rich(item)
    return result

def _wrap_composition(kind: str, body: Sequence[Content]) -> RichText:
    return RichText((_Element(kind, _compile_body(body).nodes),))

def _target_capabilities(target: PlatformCapabilities | str) -> PlatformCapabilities:
    if isinstance(target, PlatformCapabilities):
        return target
    from peyk.platform_core.adapters import BALE_CAPABILITIES, RUBIKA_CAPABILITIES, TELEGRAM_CAPABILITIES
    try:
        return {'telegram': TELEGRAM_CAPABILITIES, 'bale': BALE_CAPABILITIES, 'rubika': RUBIKA_CAPABILITIES}[target]
    except KeyError as exc:
        raise ValueError(f'unknown formatting target: {target!r}') from exc

def as_line(*items: Content, sep: str=' ') -> Text:
    """Join items on one line."""
    return Text(*_interleave(items, sep))

def as_list(*items: Content | Iterable[Content], sep: str='\n') -> Text:
    """Join items as a list separated by ``sep``; one iterable is also accepted."""
    values = _normalize_items(items)
    return Text(*_interleave(values, sep))

def as_marked_list(*items: Content | Iterable[Content], marker: str='▫️', sep: str='\n') -> Text:
    """Prefix each item with ``marker``."""
    values = _normalize_items(items)
    return as_list(*(Text(marker, ' ', item) for item in values), sep=sep)

def as_numbered_list(*items: Content | Iterable[Content], sep: str='\n') -> Text:
    """Prefix each item with its one-based position."""
    values = _normalize_items(items)
    return as_list(*(Text(f'{index}. ', item) for index, item in enumerate(values, 1)), sep=sep)

def as_section(title: Content, *body: Content, sep: str='\n') -> Text:
    """Return a title followed by body lines."""
    return Text(title, *body, sep=sep)

def as_marked_section(title: Content, *body: Content, marker: str='▫️', sep: str='\n') -> Text:
    """Return a title followed by a marked list."""
    return Text(title, as_marked_list(*body, marker=marker, sep=sep), sep=sep)

def as_key_value(key: Content, value: Content, sep: str=': ') -> Text:
    """Join a key and value with ``sep``."""
    return Text(key, value, sep=sep)

def _normalize_items(items: Sequence[Content | Iterable[Content]]) -> tuple[Content, ...]:
    if len(items) == 1 and (not isinstance(items[0], (str, RichText, Text))):
        candidate = items[0]
        if isinstance(candidate, Iterable):
            return cast(tuple[Content, ...], tuple(candidate))
    return cast(tuple[Content, ...], tuple(items))

def _interleave(items: Sequence[Content], sep: str) -> tuple[Content, ...]:
    result: list[Content] = []
    for index, item in enumerate(items):
        if index:
            result.append(sep)
        result.append(item)
    return tuple(result)

def resolve_text(content: str | RichText | Text, platform_caps: PlatformCapabilities, policy: 'UnsupportedPolicy', defaults: TextDefaults) -> tuple[str, dict[str, object]]:
    """Resolve text once at send time into target text and native keyword arguments.

    Plain strings remain plain unless a default parse mode is configured.
    Rich compositions are rendered from the neutral IR; Rubika additionally
    receives its structured metadata. Explicit parse-mode handling is applied
    by :class:`peyk.Bot` before this resolver is called.
    """
    from peyk.bot.policy import UnsupportedPolicy
    if isinstance(content, str):
        native: dict[str, object] = {}
        parse_mode = getattr(defaults, 'parse_mode', None)
        if parse_mode is not None:
            native['parse_mode'] = parse_mode.value if isinstance(parse_mode, ParseMode) else str(parse_mode)
        return (content, native)
    rich = content if isinstance(content, RichText) else content.to_rich_text()
    text = render_for(rich, platform_caps)
    if platform_caps.platform == 'rubika':
        rendered, metadata = render_rubika_metadata(rich)
        return (rendered, {'metadata': {'meta_data_parts': metadata}})
    if platform_caps.platform == 'telegram':
        return (text, {'parse_mode': 'HTML'})
    return (text, {})
__all__ = ['Text', 'Bold', 'Italic', 'Underline', 'Strikethrough', 'Spoiler', 'Code', 'Pre', 'TextLink', 'TextMention', 'BlockQuote', 'ExpandableBlockQuote', 'as_line', 'as_list', 'as_marked_list', 'as_numbered_list', 'as_section', 'as_marked_section', 'as_key_value', 'resolve_text', 'TextDefaults', 'bold', 'italic', 'underline', 'strikethrough', 'spoiler', 'code', 'pre', 'link', 'mention_user', 'mention_username', 'bale_expandable', 'ParseMode']
