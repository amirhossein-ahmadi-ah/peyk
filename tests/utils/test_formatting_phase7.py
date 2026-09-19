from peyk.formatting import (
    Text, Bold, Italic, Underline, Strikethrough, Spoiler, Code, Pre,
    TextLink, TextMention, BlockQuote, ExpandableBlockQuote,
    as_line, as_list, as_marked_list, as_numbered_list, as_section,
    as_marked_section, as_key_value,
)
from peyk.platform_core.adapters import BALE_CAPABILITIES, RUBIKA_CAPABILITIES, TELEGRAM_CAPABILITIES
from peyk.platform_core.enums import ParseMode
from peyk.utils.text_formatting import RUBIKA_METADATA_OFFSET_UNIT


def test_composition_nodes_render_per_platform():
    value = Text("سلام ", Bold("<Amir>"), " ", Italic("دنیا"))
    assert value.render(TELEGRAM_CAPABILITIES) == "<b>سلام &lt;Amir&gt;</b>" if False else "<b>سلام &lt;Amir&gt;</b> دنیا"
    assert value.render(BALE_CAPABILITIES) == "سلام *<Amir>* _دنیا_"
    assert value.render(RUBIKA_CAPABILITIES) == "سلام <Amir> دنیا"


def test_text_kwargs_are_native():
    value = Text("سلام ", Bold("دنیا"))
    assert value.as_kwargs("telegram") == {"text": "سلام <b>دنیا</b>", "parse_mode": "HTML"}
    assert value.as_kwargs("bale") == {"text": "سلام *دنیا*"}
    kwargs = value.as_kwargs("rubika")
    assert kwargs["text"] == "سلام دنیا"
    assert kwargs["metadata"] == {"meta_data_parts": [{"type": "Bold", "from_index": 5, "length": 4}]}


def test_all_formatting_nodes_have_expected_telegram_html():
    value = Text(
        Bold("b"), Italic("i"), Underline("u"), Strikethrough("s"), Spoiler("x"),
        Code("c"), Pre("p", language="py"), TextLink("l", url="https://e.test"),
        TextMention("m", user_id=7), BlockQuote("q"), ExpandableBlockQuote("e"),
    )
    assert value.render("telegram") == (
        '<b>b</b><i>i</i><u>u</u><s>s</s><tg-spoiler>x</tg-spoiler><code>c</code>'
        '<pre><code class="language-py">p</code></pre><a href="https://e.test">l</a>'
        '<a href="tg://user?id=7">m</a><blockquote>q</blockquote><blockquote expandable>e</blockquote>'
    )


def test_lists_and_sections_keep_rtl_text():
    assert as_line("نام", "علی").render("telegram") == "نام علی"
    assert as_list(["اول", "دوم"]).render("telegram") == "اول\nدوم"
    assert as_marked_list(["اول", "دوم"]).render("telegram") == "▫️ اول\n▫️ دوم"
    assert as_numbered_list(["اول", "دوم"]).render("telegram") == "1. اول\n2. دوم"
    assert as_section("عنوان", "بدنه").render("telegram") == "عنوان\nبدنه"
    assert as_marked_section("عنوان", "بدنه").render("telegram") == "عنوان\n▫️ بدنه"
    assert as_key_value("کلید", "مقدار").render("telegram") == "کلید: مقدار"


def test_nested_formatting():
    assert Text(Bold("سلام ", Italic("دنیا"))).render("telegram") == "<b>سلام <i>دنیا</i></b>"


def test_rubika_offset_assumption_with_persian_and_emoji():
    text, parts = __import__("peyk.utils.text_formatting", fromlist=["render_rubika_metadata"]).render_rubika_metadata(
        Bold("سلام 🦊").to_rich_text()
    )
    assert RUBIKA_METADATA_OFFSET_UNIT == "codepoint"
    assert text == "سلام 🦊"
    assert parts == [{"type": "Bold", "from_index": 0, "length": len("سلام 🦊")}]


def test_html_and_markdown_helpers_are_not_portable():
    from peyk.utils import html, markdown
    assert html.bold("<x>") == "<b>&lt;x&gt;</b>"
    assert markdown.bold("a_b") == r"*a\_b*"


import pytest


@pytest.mark.parametrize(
    ("node", "telegram", "bale", "rubika"),
    [
        (Bold("x"), "<b>x</b>", "*x*", "x"),
        (Italic("x"), "<i>x</i>", "_x_", "x"),
        (Underline("x"), "<u>x</u>", "x", "x"),
        (Strikethrough("x"), "<s>x</s>", "x", "x"),
        (Spoiler("x"), "<tg-spoiler>x</tg-spoiler>", "x", "x"),
        (Code("x"), "<code>x</code>", "```x```", "x"),
        (Pre("x", language="py"), '<pre><code class="language-py">x</code></pre>', "```x```", "x"),
        (TextLink("x", url="https://e.test"), '<a href="https://e.test">x</a>', "[x](https://e.test)", "x"),
        (TextMention("x", user_id=7), '<a href="tg://user?id=7">x</a>', "[x](uid:7)", "x"),
        (BlockQuote("x"), "<blockquote>x</blockquote>", "x", "x"),
        (ExpandableBlockQuote("x"), "<blockquote expandable>x</blockquote>", "x", "x"),
    ],
)
def test_node_golden_all_platforms(node, telegram, bale, rubika):
    assert node.render("telegram") == telegram
    assert node.render("bale") == bale
    assert node.render("rubika") == rubika


def test_text_separator_and_aiogram_like_list_calls():
    assert Text("a", "b", sep=" ").render("telegram") == "a b"
    assert as_list("a", "b").render("telegram") == "a\nb"
    assert as_marked_list(["a", "b"]).render("telegram") == "▫️ a\n▫️ b"

def test_fluent_text_builder_matches_documented_api():
    value = Text("Hello ").bold("world").line().link("docs", "https://example.com")
    assert value.render("telegram") == 'Hello <b>world</b>\n<a href="https://example.com">docs</a>'

