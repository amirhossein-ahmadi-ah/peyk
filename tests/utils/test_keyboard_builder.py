import pytest

from peyk.utils.keyboard_builder import KeyboardBuildError, KeyboardBuilder


def test_simple_keyboard_builds_for_all_three_platforms():
    builder = KeyboardBuilder().button("OK", callback_data="ok").row().button("Docs", url="https://example.com")
    telegram = builder.build("telegram")
    assert telegram.to_dict() == {"inline_keyboard": [[{"text": "OK", "callback_data": "ok"}], [{"text": "Docs", "url": "https://example.com"}]]}
    bale = builder.build("bale")
    assert [[(b.text, b.callback_data, b.url) for b in row] for row in bale.inline_keyboard] == [[("OK", "ok", None)], [("Docs", None, "https://example.com")]]
    rubika = builder.build("rubika")
    assert rubika.to_dict()["rows"][0]["buttons"][0]["type"] == "Simple"
    assert rubika.to_dict()["rows"][1]["buttons"][0]["type"] == "Link"


def test_bale_and_telegram_reply_buttons():
    builder = KeyboardBuilder().reply_button("📍 موقعیت", request_location=True).row().reply_button("☎️ شماره", request_contact=True)
    for target in ("telegram", "bale"):
        built = builder.build(target)
        assert built.keyboard[0][0].request_location is True
        assert built.keyboard[1][0].request_contact is True


def test_all_rubika_button_types_are_constructible():
    methods = [
        lambda b: b.selection("S", button_id="s", selection_id="sel", items=[{"text": "A"}]),
        lambda b: b.calendar("C", button_id="c"),
        lambda b: b.number_picker("N", button_id="n"),
        lambda b: b.string_picker("SP", button_id="sp", items=["A", "B"]),
        lambda b: b.location("L", button_id="l"),
        lambda b: b.camera_image("CI", button_id="ci"),
        lambda b: b.camera_video("CV", button_id="cv"),
        lambda b: b.gallery_image("GI", button_id="gi"),
        lambda b: b.gallery_video("GV", button_id="gv"),
        lambda b: b.file("F", button_id="f"),
        lambda b: b.audio("A", button_id="a"),
        lambda b: b.record_audio("RA", button_id="ra"),
        lambda b: b.textbox("T", button_id="t"),
        lambda b: b.rubika_link("Link", button_id="link", url="https://example.com"),
        lambda b: b.ask_my_phone_number("Phone", button_id="phone"),
        lambda b: b.ask_my_location("Loc", button_id="loc"),
        lambda b: b.barcode("Barcode", button_id="barcode"),
    ]
    builder = KeyboardBuilder()
    for method in methods:
        method(builder).row()
    built = builder.build("rubika").to_dict()
    types = [row["buttons"][0]["type"] for row in built["rows"]]
    assert types == [
        "Selection", "Calendar", "NumberPicker", "StringPicker", "Location",
        "CameraImage", "CameraVideo", "GalleryImage", "GalleryVideo", "File",
        "Audio", "RecordAudio", "Textbox", "Link", "AskMyPhoneNumber",
        "AskMyLocation", "Barcode",
    ]


def test_rubika_specific_button_types_are_rejected_elsewhere():
    with pytest.raises(KeyboardBuildError, match="Rubika-only"):
        KeyboardBuilder().calendar("Pick date").build("telegram")
    with pytest.raises(KeyboardBuildError, match="Rubika-only"):
        KeyboardBuilder().calendar("Pick date").build("bale")


def test_callback_data_uses_platform_byte_limit_at_build_time():
    value = "ی" * 33
    for target in ("telegram", "bale"):
        with pytest.raises(KeyboardBuildError, match="1-64 bytes"):
            KeyboardBuilder().button("bad", callback_data=value).build(target)
    built = KeyboardBuilder().button("long", callback_data="x" * 500).build("rubika")
    assert built.to_dict()["rows"][0]["buttons"][0]["id"] == "x" * 500
