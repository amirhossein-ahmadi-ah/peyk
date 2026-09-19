"""Platform-neutral rich text with explicit Bale markup and plain Rubika output."""
from __future__ import annotations
from dataclasses import dataclass, field
from html import escape as html_escape
from typing import Optional, Union
from peyk.platform_core.contracts import PlatformCapabilities

@dataclass(frozen=True)
class _Text:
    value: str

@dataclass(frozen=True)
class _Element:
    kind: str
    children: tuple['Node', ...]
    url: Optional[str] = None
    user_id: Optional[int | str] = None
    username: Optional[str] = None
    language: Optional[str] = None
Node = Union[_Text, _Element]

@dataclass(frozen=True)
class RichText:
    """Immutable, composable rich-text intermediate representation.

    Example:
        .. code-block:: python

            text = RichText.from_value("Hello ") + bold("world")
            rendered = text.render("bale")
    """
    nodes: tuple[Node, ...] = field(default_factory=tuple)

    @classmethod
    def from_value(cls, value: Union[str, 'RichText']) -> 'RichText':
        """Performs the from value operation for the utility client.

Args:
    value: Value used by this operation.

Returns:
    Result produced by the utility operation."""
        "Executes the from_value operation.\n                \n                Args:\n                    value: Value of the declared parameter type.\n                \n                \n                Returns:\n                    The operation result (``'RichText'``).\n                \n        \n        Raises:\n            TypeError: Raised when the operation cannot complete.\n        "
        if isinstance(value, RichText):
            return value
        if not isinstance(value, str):
            raise TypeError('rich text content must be str or RichText')
        return cls((_Text(value),))

    def plain_text(self) -> str:
        """Performs the plain text operation for the utility client.

Returns:
    Result produced by the utility operation."""
        'Executes the plain_text operation.\n        \n        Returns:\n            The operation result (``str``).\n        '
        return ''.join((_plain(node) for node in self.nodes))

    def __add__(self, other: Union[str, 'RichText']) -> 'RichText':
        rhs = RichText.from_value(other)
        return RichText(self.nodes + rhs.nodes)

def _plain(node: Node) -> str:
    if isinstance(node, _Text):
        return node.value
    return ''.join((_plain(child) for child in node.children))

def _wrap(kind: str, value: Union[str, RichText], **kwargs: object) -> RichText:
    rich = RichText.from_value(value)
    return RichText((_Element(kind, rich.nodes, **kwargs),))

def bold(text: Union[str, RichText]) -> RichText:
    """Performs the bold operation for the utility client.

Args:
    text: Text content supplied to the operation.

Returns:
    Result produced by the utility operation."""
    'Executes the bold operation.\n    \n    Args:\n        text: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``RichText``).\n    '
    return _wrap('bold', text)

def italic(text: Union[str, RichText]) -> RichText:
    """Performs the italic operation for the utility client.

Args:
    text: Text content supplied to the operation.

Returns:
    Result produced by the utility operation."""
    'Executes the italic operation.\n    \n    Args:\n        text: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``RichText``).\n    '
    return _wrap('italic', text)

def link(text: Union[str, RichText], url: str) -> RichText:
    """Performs the link operation for the utility client.

Args:
    text: Text content supplied to the operation.
    url: Target URL.

Returns:
    Result produced by the utility operation."""
    'Executes the link operation.\n        \n        Args:\n            text: Value of the declared parameter type.\n            url: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``RichText``).\n        \n    \n    Raises:\n        ValueError: Raised when the operation cannot complete.\n    '
    if not isinstance(url, str) or not url:
        raise ValueError('url must be a non-empty string')
    return _wrap('link', text, url=url)

def mention_user(text: Union[str, RichText], user_id: int | str) -> RichText:
    """Performs the mention user operation for the utility client.

Args:
    text: Text content supplied to the operation.
    user_id: Identifier of the target user.

Returns:
    Result produced by the utility operation."""
    'Bale numeric-user mention: ``[name](uid:user_id)``.\n        \n        Args:\n            text: Value of the declared parameter type.\n            user_id: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``RichText``).\n        \n    \n    Raises:\n        ValueError: Raised when the operation cannot complete.\n    '
    if user_id is None or str(user_id) == '':
        raise ValueError('user_id must not be empty')
    return _wrap('mention_user', text, user_id=user_id)

def mention_username(text: Union[str, RichText], username: str) -> RichText:
    """Performs the mention username operation for the utility client.

Args:
    text: Text content supplied to the operation.
    username: Value used by this operation.

Returns:
    Result produced by the utility operation."""
    'Bale username mention: ``[name](ble.ir/username)``.\n        \n        Args:\n            text: Value of the declared parameter type.\n            username: Value of the declared parameter type.\n        \n        \n        Returns:\n            The operation result (``RichText``).\n        \n    \n    Raises:\n        ValueError: Raised when the operation cannot complete.\n    '
    username = username.lstrip('@').strip()
    if not username:
        raise ValueError('username must not be empty')
    return _wrap('mention_username', text, username=username)

def code(text: Union[str, RichText]) -> RichText:
    """Performs the code operation for the utility client.

Args:
    text: Text content supplied to the operation.

Returns:
    Result produced by the utility operation."""
    'Executes the code operation.\n    \n    Args:\n        text: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``RichText``).\n    '
    return _wrap('code', text)

def pre(text: Union[str, RichText], language: str | None=None) -> RichText:
    """Performs the pre operation for the utility client.

Args:
    text: Text content supplied to the operation.
    language: Value used by this operation.

Returns:
    Result produced by the utility operation."""
    'Executes the pre operation.\n    \n    Args:\n        text: Value of the declared parameter type.\n        language: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``RichText``).\n    '
    return _wrap('pre', text, language=language)

def underline(text: Union[str, RichText]) -> RichText:
    """Performs the underline operation for the utility client.

Args:
    text: Text content supplied to the operation.

Returns:
    Result produced by the utility operation."""
    'Executes the underline operation.\n    \n    Args:\n        text: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``RichText``).\n    '
    return _wrap('underline', text)

def strikethrough(text: Union[str, RichText]) -> RichText:
    """Performs the strikethrough operation for the utility client.

Args:
    text: Text content supplied to the operation.

Returns:
    Result produced by the utility operation."""
    'Executes the strikethrough operation.\n    \n    Args:\n        text: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``RichText``).\n    '
    return _wrap('strikethrough', text)

def spoiler(text: Union[str, RichText]) -> RichText:
    """Performs the spoiler operation for the utility client.

Args:
    text: Text content supplied to the operation.

Returns:
    Result produced by the utility operation."""
    'Executes the spoiler operation.\n    \n    Args:\n        text: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``RichText``).\n    '
    return _wrap('spoiler', text)

def bale_expandable(title: str, text: Union[str, RichText]) -> RichText:
    """Performs the bale expandable operation for the utility client.

Args:
    title: Title to apply to the target resource.
    text: Text content supplied to the operation.

Returns:
    Result produced by the utility operation."""
    "Bale's copy-friendly expanded page form: ``[title]```content``` ``.\n    \n    Args:\n        title: Value of the declared parameter type.\n        text: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``RichText``).\n    "
    return _wrap('bale_expandable', text, url=title)
RUBIKA_METADATA_OFFSET_UNIT = 'codepoint'

def _render_html(node: Node) -> str:
    if isinstance(node, _Text):
        return html_escape(node.value, quote=False)
    body = ''.join((_render_html(child) for child in node.children))
    if node.kind == 'bold':
        return f'<b>{body}</b>'
    if node.kind == 'italic':
        return f'<i>{body}</i>'
    if node.kind == 'underline':
        return f'<u>{body}</u>'
    if node.kind == 'strikethrough':
        return f'<s>{body}</s>'
    if node.kind == 'spoiler':
        return f'<tg-spoiler>{body}</tg-spoiler>'
    if node.kind == 'code':
        return f'<code>{body}</code>'
    if node.kind == 'blockquote':
        return f'<blockquote>{body}</blockquote>'
    if node.kind == 'expandable_blockquote':
        return f'<blockquote expandable>{body}</blockquote>'
    if node.kind == 'pre':
        if node.language:
            language = html_escape(node.language, quote=True)
            return f'<pre><code class="language-{language}">{body}</code></pre>'
        return f'<pre>{body}</pre>'
    if node.kind in {'link', 'mention_user', 'mention_username'}:
        if node.kind == 'link':
            href = node.url or ''
        elif node.kind == 'mention_user':
            href = f'tg://user?id={node.user_id}'
        else:
            href = f'https://t.me/{node.username}'
        return f'<a href="{html_escape(href, quote=True)}">{body}</a>'
    return body

def _mdv2_escape(text: str) -> str:
    return ''.join(('\\' + ch if ch in '_[]()~`>#+-=|{}.!' else ch for ch in text))

def _render_mdv2(node: Node) -> str:
    if isinstance(node, _Text):
        return _mdv2_escape(node.value)
    body = ''.join((_render_mdv2(child) for child in node.children))
    if node.kind == 'bold':
        return f'*{body}*'
    if node.kind == 'italic':
        return f'_{body}_'
    if node.kind == 'underline':
        return f'__{body}__'
    if node.kind == 'strikethrough':
        return f'~{body}~'
    if node.kind == 'spoiler':
        return f'||{body}||'
    if node.kind == 'code':
        escaped = _plain(node).replace('`', '\\`')
        return f'`{escaped}`'
    if node.kind == 'blockquote':
        return '\n'.join(('> ' + line for line in _plain(node).splitlines()))
    if node.kind == 'expandable_blockquote':
        return '\n'.join(('> ' + line for line in _plain(node).splitlines()))
    if node.kind == 'pre':
        raw = _plain(node).replace('`', '\\`')
        return f"```{node.language or ''}\n{raw}\n```"
    if node.kind == 'link':
        url = (node.url or '').replace('\\', '\\\\').replace(')', '\\)')
        return f'[{body}]({url})'
    if node.kind == 'mention_user':
        return f'[{body}](tg://user?id={node.user_id})'
    if node.kind == 'mention_username':
        return f'[{body}](https://t.me/{node.username})'
    return body

def _render_markdown(node: Node) -> str:
    if isinstance(node, _Text):
        return node.value.replace('\\', '\\\\').replace('`', '\\`').replace('*', '\\*').replace('_', '\\_')
    body = ''.join((_render_markdown(child) for child in node.children))
    if node.kind == 'bold':
        return f'*{body}*'
    if node.kind == 'italic':
        return f'_{body}_'
    if node.kind == 'code':
        return f'`{_plain(node)}`'
    if node.kind == 'pre':
        return f'```{_plain(node)}\n```'
    if node.kind == 'link':
        return f"[{body}]({node.url or ''})"
    if node.kind == 'mention_user':
        return f'[{body}](tg://user?id={node.user_id})'
    if node.kind == 'blockquote':
        return '\n'.join(('> ' + line for line in _plain(node).splitlines()))
    if node.kind == 'expandable_blockquote':
        return '\n'.join(('> ' + line for line in _plain(node).splitlines()))
    return body

def _render_bale(node: Node) -> str:
    """Render Bale's inline markup; this is NOT a Telegram-style parse_mode."""
    if isinstance(node, _Text):
        return node.value
    body = ''.join((_render_bale(child) for child in node.children))
    if node.kind == 'bold':
        return f'*{body}*'
    if node.kind == 'italic':
        return f'_{body}_'
    if node.kind == 'link':
        return f'[{body}]({node.url})'
    if node.kind == 'mention_user':
        return f'[{body}](uid:{node.user_id})'
    if node.kind == 'mention_username':
        return f'[{body}](ble.ir/{node.username})'
    if node.kind == 'code':
        return f'```{body}```'
    if node.kind == 'pre':
        return f'```{body}```'
    if node.kind == 'bale_expandable':
        return f"[{node.url or ''}]```{body}```"
    return body

def render_for(rich_text: RichText, capabilities: PlatformCapabilities) -> str:
    """Performs the render for operation for the utility client.

Args:
    rich_text: Value used by this operation.
    capabilities: Value used by this operation.

Returns:
    Result produced by the utility operation."""
    "Render according to the target platform's confirmed text model.\n    \n        Telegram uses its advertised parse modes. Bale uses its documented/project\n        markup syntax without pretending it has Telegram's ``parse_mode`` field.\n        Rubika intentionally returns plain text here; its metadata representation\n        remains an explicit opt-in API helper.\n        \n    \n    Args:\n        rich_text: Value of the declared parameter type.\n        capabilities: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``str``).\n    "
    rich = RichText.from_value(rich_text)
    if capabilities.platform == 'bale':
        return ''.join((_render_bale(node) for node in rich.nodes))
    if capabilities.platform == 'rubika':
        return rich.plain_text()
    modes = {mode.lower(): mode for mode in capabilities.supported_parse_modes}
    if 'html' in modes:
        return ''.join((_render_html(node) for node in rich.nodes))
    if 'markdownv2' in modes:
        return ''.join((_render_mdv2(node) for node in rich.nodes))
    if 'markdown' in modes:
        return ''.join((_render_markdown(node) for node in rich.nodes))
    return rich.plain_text()

def render_rubika_metadata(rich_text: RichText) -> tuple[str, list[dict[str, object]]]:
    """Performs the render rubika metadata operation for the utility client.

Args:
    rich_text: Value used by this operation.

Returns:
    Result produced by the utility operation."""
    'Optional explicit Rubika metadata renderer; never selected by parse mode.\n    \n    Args:\n        rich_text: Value of the declared parameter type.\n    \n    \n    Returns:\n        The operation result (``tuple[str, list[dict[str, object]]]``).\n    '
    rich = RichText.from_value(rich_text)
    text = rich.plain_text()
    parts: list[dict[str, object]] = []
    offset = 0
    for node in rich.nodes:
        offset = _collect_metadata(node, offset, parts)
    return (text, parts)

def _collect_metadata(node: Node, offset: int, parts: list[dict[str, object]]) -> int:
    if isinstance(node, _Text):
        return offset + len(node.value)
    start = offset
    for child in node.children:
        offset = _collect_metadata(child, offset, parts)
    type_map = {'bold': 'Bold', 'italic': 'Italic', 'code': 'Mono', 'pre': 'Pre', 'underline': 'Underline', 'strikethrough': 'Strike', 'spoiler': 'Spoiler', 'link': 'Link', 'mention_user': 'MentionText', 'blockquote': 'Quote', 'expandable_blockquote': 'Quote'}
    if node.kind in type_map and offset > start:
        part: dict[str, object] = {'type': type_map[node.kind], 'from_index': start, 'length': offset - start}
        if node.kind == 'link':
            part['link_url'] = node.url or ''
        if node.kind == 'mention_user':
            part['mention_text_user_id'] = str(node.user_id)
        parts.append(part)
    return offset
__all__ = ['RichText', 'bold', 'italic', 'link', 'mention_user', 'mention_username', 'code', 'pre', 'underline', 'strikethrough', 'spoiler', 'bale_expandable', 'render_for', 'render_rubika_metadata', 'RUBIKA_METADATA_OFFSET_UNIT']
