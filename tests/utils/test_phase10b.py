import hashlib,hmac
from peyk.flags import flags,get_flag,check_flags
from peyk.utils.deep_linking import encode_payload,decode_payload
from peyk.utils.web_app import check_webapp_signature,safe_parse_webapp_init_data

def test_flags_and_deeplink_roundtrip():
    @flags.chat_action("typing")
    def handler(): pass
    assert get_flag(handler,"chat_action") == "typing"
    assert check_flags({"chat_action":"typing"},{"chat_action":"typing"})
    value=encode_payload("سلام world")
    assert decode_payload(value)=="سلام world"

def test_webapp_signature_vector_roundtrip():
    token="123456:ABC"
    data="auth_date=1662771648\nquery_id=AAHdF6IQ\nuser={\"id\":1}"
    secret=hmac.new(b"WebAppData",token.encode(),hashlib.sha256).digest()
    digest=hmac.new(secret,data.encode(),hashlib.sha256).hexdigest()
    from urllib.parse import quote
    init="auth_date=1662771648&query_id=AAHdF6IQ&user="+quote('{"id":1}')+"&hash="+digest
    assert check_webapp_signature(init,token)
    assert safe_parse_webapp_init_data(init,token)["auth_date"]=="1662771648"
from peyk.utils.i18n import I18n

def test_i18n_persian_and_locale_switching():
    i18n=I18n("tests/fixtures/i18n", default_locale="fa")
    assert i18n.gettext("Hello")=="سلام"
    assert i18n.ngettext("One item", "%d items", 1)=="یک مورد"
    i18n.set_locale("en")
    assert i18n.gettext("Hello")=="Hello"
