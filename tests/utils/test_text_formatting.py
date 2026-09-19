from peyk.platform_core.adapters import BALE_CAPABILITIES, RUBIKA_CAPABILITIES, TELEGRAM_CAPABILITIES
from peyk.utils.text_formatting import (
    bale_expandable, bold, code, italic, link, mention_user, mention_username,
    pre, render_for, render_rubika_metadata, spoiler, strikethrough, underline,
)


def test_rich_text_composes_and_renders_for_telegram_html():
    rich = bold("hello ") + italic("world") + " " + link(code("docs"), "https://example.com")
    rich = rich + " " + underline("u") + " " + strikethrough("s") + " " + spoiler("secret")
    assert render_for(rich, TELEGRAM_CAPABILITIES) == '<b>hello </b><i>world</i> <a href="https://example.com"><code>docs</code></a> <u>u</u> <s>s</s> <tg-spoiler>secret</tg-spoiler>'


def test_telegram_pre_language():
    assert render_for(pre("print(1)", "python"), TELEGRAM_CAPABILITIES) == '<pre><code class="language-python">print(1)</code></pre>'


def test_bale_project_markup_is_not_parse_mode():
    rich = (
        bold("bold") + " " + italic("italic") + " " + link("site", "https://example.com") + " "
        + mention_user("Amir", 12345) + " " + mention_username("User", "someone") + " "
        + pre("print(1)") + " " + bale_expandable("باز کن", "copy me")
    )
    assert render_for(rich, BALE_CAPABILITIES) == (
        "*bold* _italic_ [site](https://example.com) [Amir](uid:12345) "
        "[User](ble.ir/someone) ```print(1)``` [باز کن]```copy me```"
    )


def test_bale_unsupported_rich_nodes_are_stripped_without_literal_markup():
    assert render_for(underline("u") + strikethrough("s") + spoiler("x"), BALE_CAPABILITIES) == "usx"


def test_rubika_is_plain_text_in_render_for():
    assert render_for(bold("hello") + italic("world"), RUBIKA_CAPABILITIES) == "helloworld"


def test_rubika_metadata_remains_explicit_opt_in():
    text, parts = render_rubika_metadata(bold("hello") + " " + link("site", "https://example.com"))
    assert text == "hello site"
    assert parts == [
        {"type": "Bold", "from_index": 0, "length": 5},
        {"type": "Link", "from_index": 6, "length": 4, "link_url": "https://example.com"},
    ]
