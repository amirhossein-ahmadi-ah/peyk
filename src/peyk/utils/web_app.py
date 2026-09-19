from __future__ import annotations
import hashlib,hmac
from urllib.parse import parse_qsl

def check_webapp_signature(init_data: str, bot_token: str) -> bool:
    """Validate Telegram Web App init data according to the documented HMAC scheme."""
    values = dict(parse_qsl(init_data, keep_blank_values=True)); received = values.pop("hash", None)
    if not received: return False
    check = "\n".join(f"{k}={v}" for k,v in sorted(values.items()))
    secret = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
    return hmac.compare_digest(hmac.new(secret, check.encode(), hashlib.sha256).hexdigest(), received)
def safe_parse_webapp_init_data(init_data: str, bot_token: str) -> dict[str,str]:
    """Validate and parse Telegram Web App init data."""
    if not check_webapp_signature(init_data, bot_token): raise ValueError("Invalid Telegram Web App init data signature")
    return dict(parse_qsl(init_data, keep_blank_values=True))
