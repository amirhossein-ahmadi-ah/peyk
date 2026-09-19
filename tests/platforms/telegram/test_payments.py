"""Tests for `TelegramClient` payments & Stars methods (Phase T11).

Fake `aiohttp.test_utils` server, zero real network. Covers:
- `send_invoice` / `create_invoice_link` — both traditional and Stars (XTR)
- `answer_shipping_query` / `answer_pre_checkout_query` — success and failure paths
- `get_star_transactions`, `refund_star_payment`, `edit_user_star_subscription`
- `send_paid_media` — JSON and multipart paths
- `SuccessfulPayment` parsing embedded in a fake `Message`
- `TransactionPartner` tagged-union parsing for multiple subtypes
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

import orjson
import pytest
from aiohttp import web
from aiohttp.test_utils import TestServer

from peyk.platforms.telegram.client import TelegramClient
from peyk.platforms.telegram.models import (
    Invoice,
    LabeledPrice,
    Message,
    PaidMediaInfo,
    PaidMediaPhoto,
    PaidMediaPreview,
    PaidMediaVideo,
    PhotoSize,
    PreCheckoutQuery,
    RefundedPayment,
    ShippingAddress,
    ShippingOption,
    ShippingQuery,
    StarTransaction,
    StarTransactions,
    SuccessfulPayment,
    TransactionPartnerFragment,
    TransactionPartnerOther,
    TransactionPartnerTelegramAds,
    TransactionPartnerUser,
    User,
    Video,
)
from peyk.transport import RetryPolicy

TOKEN = "12345:TEST-TOKEN"

SAMPLE_USER_RAW = {
    "id": 100,
    "is_bot": True,
    "first_name": "TestBot",
    "username": "test_bot",
}

SAMPLE_CHAT_RAW = {
    "id": 200,
    "type": "private",
    "first_name": "Some",
    "last_name": "One",
    "username": "someone",
}


def _sample_message_raw(message_id: int = 1, **extra: Any) -> Dict[str, Any]:
    base: Dict[str, Any] = {
        "message_id": message_id,
        "date": 1690000000,
        "chat": SAMPLE_CHAT_RAW,
        "from": SAMPLE_USER_RAW,
    }
    base.update(extra)
    return base


class FakeTelegramServer:
    def __init__(self) -> None:
        self.responses: Dict[str, Callable[[Any], Any]] = {}
        self.request_log: List[Dict[str, Any]] = []
        self.app = web.Application()
        self.app.router.add_route("*", "/bot{token}/{method}", self._handle)

    def set_response(
        self, method_name: str, result_builder: Callable[[Any], Any]
    ) -> None:
        self.responses[method_name] = result_builder

    async def _handle(self, request: web.Request) -> web.Response:
        method_name = request.match_info["method"]
        token = request.match_info["token"]
        content_type = request.headers.get("Content-Type", "")
        if "multipart/form-data" in content_type:
            reader = await request.multipart()
            fields: Dict[str, str] = {}
            files: Dict[str, Dict[str, Any]] = {}
            async for part in reader:
                if part.filename:
                    files[part.name] = {
                        "filename": part.filename,
                        "content": await part.read(decode=False),
                    }
                else:
                    fields[part.name] = await part.text()
            parsed_body: Any = {
                "multipart": True,
                "fields": fields,
                "files": files,
            }
        else:
            raw = await request.read()
            parsed_body = orjson.loads(raw) if raw else {}
        self.request_log.append(
            {
                "method_name": method_name,
                "token": token,
                "http_method": request.method,
                "body": parsed_body,
            }
        )
        builder = self.responses.get(method_name)
        result = builder(parsed_body) if builder else None
        return web.json_response({"ok": True, "result": result})

    def calls_for(self, method_name: str) -> List[Dict[str, Any]]:
        return [c for c in self.request_log if c["method_name"] == method_name]


@pytest.fixture
async def fake_server():
    server = FakeTelegramServer()
    async with TestServer(server.app) as test_server:
        yield server, test_server


def _client_for(test_server: TestServer) -> TelegramClient:
    base_url = str(test_server.make_url("")).rstrip("/")
    return TelegramClient(
        TOKEN,
        base_url=base_url,
        retry_policy=RetryPolicy(max_attempts=3, base_backoff_seconds=0.001),
    )


# ---------------------------------------------------------------------------
# send_invoice
# ---------------------------------------------------------------------------


async def test_send_invoice_traditional(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendInvoice",
        lambda body: _sample_message_raw(1, invoice={
            "title": "Test Product",
            "description": "A test product",
            "start_parameter": "start",
            "currency": "USD",
            "total_amount": 1000,
        }),
    )
    client = _client_for(test_server)
    try:
        msg = await client.send_invoice(
            200,
            title="Test Product",
            description="A test product",
            payload="invoice_payload_123",
            currency="USD",
            prices=[LabeledPrice(label="Price", amount=1000)],
        )
    finally:
        await client.close()
    assert isinstance(msg, Message)
    body = server.calls_for("sendInvoice")[0]["body"]
    assert body["chat_id"] == 200
    assert body["title"] == "Test Product"
    assert body["currency"] == "USD"
    assert body["prices"] == [{"label": "Price", "amount": 1000}]
    assert msg.invoice is not None
    assert msg.invoice.currency == "USD"


async def test_send_invoice_stars(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendInvoice", lambda body: _sample_message_raw(1))
    client = _client_for(test_server)
    try:
        msg = await client.send_invoice(
            200,
            title="Stars Product",
            description="A product paid in Stars",
            payload="stars_payload",
            currency="XTR",
            prices=[LabeledPrice(label="Stars", amount=100)],
        )
    finally:
        await client.close()
    body = server.calls_for("sendInvoice")[0]["body"]
    assert body["currency"] == "XTR"
    assert body["prices"] == [{"label": "Stars", "amount": 100}]


# ---------------------------------------------------------------------------
# create_invoice_link
# ---------------------------------------------------------------------------


async def test_create_invoice_link_traditional(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "createInvoiceLink",
        lambda body: "https://t.me/invoice/abc123",
    )
    client = _client_for(test_server)
    try:
        link = await client.create_invoice_link(
            title="Test Product",
            description="A test product",
            payload="invoice_payload_123",
            currency="USD",
            prices=[LabeledPrice(label="Price", amount=1000)],
        )
    finally:
        await client.close()
    assert link == "https://t.me/invoice/abc123"
    body = server.calls_for("createInvoiceLink")[0]["body"]
    assert body["currency"] == "USD"


async def test_create_invoice_link_stars(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "createInvoiceLink",
        lambda body: "https://t.me/invoice/xyz789",
    )
    client = _client_for(test_server)
    try:
        link = await client.create_invoice_link(
            title="Stars Product",
            description="Stars-paid product",
            payload="stars_payload",
            currency="XTR",
            prices=[LabeledPrice(label="Stars", amount=50)],
        )
    finally:
        await client.close()
    assert link == "https://t.me/invoice/xyz789"
    body = server.calls_for("createInvoiceLink")[0]["body"]
    assert body["currency"] == "XTR"


# ---------------------------------------------------------------------------
# answer_shipping_query
# ---------------------------------------------------------------------------


async def test_answer_shipping_query_success(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("answerShippingQuery", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.answer_shipping_query(
            "query_123",
            ok=True,
            shipping_options=[
                ShippingOption(
                    id="opt1",
                    title="Standard",
                    prices=[LabeledPrice(label="Shipping", amount=100)],
                )
            ],
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("answerShippingQuery")[0]["body"]
    assert body["shipping_query_id"] == "query_123"
    assert body["ok"] is True
    assert body["shipping_options"][0]["id"] == "opt1"


async def test_answer_shipping_query_error(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("answerShippingQuery", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.answer_shipping_query(
            "query_456",
            ok=False,
            error_message="Cannot ship to this address",
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("answerShippingQuery")[0]["body"]
    assert body["shipping_query_id"] == "query_456"
    assert body["ok"] is False
    assert body["error_message"] == "Cannot ship to this address"


# ---------------------------------------------------------------------------
# answer_pre_checkout_query
# ---------------------------------------------------------------------------


async def test_answer_pre_checkout_query_success(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("answerPreCheckoutQuery", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.answer_pre_checkout_query("query_789", ok=True)
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("answerPreCheckoutQuery")[0]["body"]
    assert body["pre_checkout_query_id"] == "query_789"
    assert body["ok"] is True


async def test_answer_pre_checkout_query_error(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("answerPreCheckoutQuery", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.answer_pre_checkout_query(
            "query_000",
            ok=False,
            error_message="Payment failed",
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("answerPreCheckoutQuery")[0]["body"]
    assert body["pre_checkout_query_id"] == "query_000"
    assert body["ok"] is False
    assert body["error_message"] == "Payment failed"


# ---------------------------------------------------------------------------
# get_star_transactions
# ---------------------------------------------------------------------------


async def test_get_star_transactions(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "getStarTransactions",
        lambda body: {
            "transactions": [
                {
                    "id": "tx1",
                    "amount": 100,
                    "date": 1700000000,
                    "source": {"type": "user"},
                    "receiver": {"type": "other"},
                }
            ]
        },
    )
    client = _client_for(test_server)
    try:
        result = await client.get_star_transactions()
    finally:
        await client.close()
    assert isinstance(result, StarTransactions)
    assert len(result.transactions) == 1
    assert result.transactions[0].id == "tx1"
    assert result.transactions[0].amount == 100


# ---------------------------------------------------------------------------
# refund_star_payment
# ---------------------------------------------------------------------------


async def test_refund_star_payment(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("refundStarPayment", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.refund_star_payment(
            user_id=100,
            telegram_payment_charge_id="charge_abc",
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("refundStarPayment")[0]["body"]
    assert body["user_id"] == 100
    assert body["telegram_payment_charge_id"] == "charge_abc"


# ---------------------------------------------------------------------------
# edit_user_star_subscription
# ---------------------------------------------------------------------------


async def test_edit_user_star_subscription(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("editUserStarSubscription", lambda body: True)
    client = _client_for(test_server)
    try:
        result = await client.edit_user_star_subscription(
            user_id=100,
            telegram_payment_charge_id="sub_123",
            is_canceled=True,
        )
    finally:
        await client.close()
    assert result is True
    body = server.calls_for("editUserStarSubscription")[0]["body"]
    assert body["user_id"] == 100
    assert body["telegram_payment_charge_id"] == "sub_123"
    assert body["is_canceled"] is True


# ---------------------------------------------------------------------------
# send_paid_media
# ---------------------------------------------------------------------------


async def test_send_paid_media_json(fake_server) -> None:
    server, test_server = fake_server
    server.set_response(
        "sendPaidMedia",
        lambda body: _sample_message_raw(1, paid_media={
            "star_count": 100,
            "paid_media": [
                {"type": "photo", "photo": [{"file_id": "p1", "file_unique_id": "p1u", "width": 100, "height": 100}]},
            ],
        }),
    )
    client = _client_for(test_server)
    try:
        from peyk.platforms.telegram.models import InputPaidMediaPhoto
        msg = await client.send_paid_media(
            200,
            star_count=100,
            media=[
                InputPaidMediaPhoto(media="FILE_ID_1"),
            ],
            caption="Premium content",
        )
    finally:
        await client.close()
    assert isinstance(msg, Message)
    body = server.calls_for("sendPaidMedia")[0]["body"]
    assert body["chat_id"] == 200
    assert body["star_count"] == 100
    assert body["caption"] == "Premium content"
    assert body["media"][0]["type"] == "photo"
    assert body["media"][0]["media"] == "FILE_ID_1"


async def test_send_paid_media_upload(fake_server) -> None:
    server, test_server = fake_server
    server.set_response("sendPaidMedia", lambda body: _sample_message_raw(1))
    client = _client_for(test_server)
    try:
        from peyk.platforms.telegram.models import InputPaidMediaVideo
        await client.send_paid_media(
            200,
            star_count=200,
            media=[
                InputPaidMediaVideo(media=b"VIDEO_DATA", duration=30),
            ],
        )
    finally:
        await client.close()
    body = server.calls_for("sendPaidMedia")[0]["body"]
    assert body["multipart"] is True
    assert body["fields"]["star_count"] == "200"
    media = orjson.loads(body["fields"]["media"])
    assert media[0]["type"] == "video"
    assert media[0]["media"].startswith("attach://")
    assert body["files"]["file0_paid_media"]["content"] == b"VIDEO_DATA"


# ---------------------------------------------------------------------------
# SuccessfulPayment parsing in Message
# ---------------------------------------------------------------------------


def test_successful_payment_traditional_in_message() -> None:
    """SuccessfulPayment embedded in a Message (traditional currency)."""
    msg = Message.from_dict(
        _sample_message_raw(
            1,
            successful_payment={
                "currency": "USD",
                "total_amount": 1000,
                "invoice_payload": "payload_123",
                "telegram_payment_charge_id": "tg_charge_1",
                "provider_payment_charge_id": "prov_charge_1",
                "shipping_option_id": "opt1",
            },
        )
    )
    assert msg.successful_payment is not None
    assert msg.successful_payment.currency == "USD"
    assert msg.successful_payment.total_amount == 1000
    assert msg.successful_payment.telegram_payment_charge_id == "tg_charge_1"
    assert msg.successful_payment.provider_payment_charge_id == "prov_charge_1"
    assert msg.successful_payment.shipping_option_id == "opt1"


def test_successful_payment_stars_in_message() -> None:
    """SuccessfulPayment embedded in a Message (Stars currency XTR)."""
    msg = Message.from_dict(
        _sample_message_raw(
            2,
            successful_payment={
                "currency": "XTR",
                "total_amount": 500,
                "invoice_payload": "stars_payload",
                "telegram_payment_charge_id": "tg_charge_2",
                "provider_payment_charge_id": "",
                "subscription_expiration_date": 1700000000,
                "is_recurring": True,
                "is_first_recurring": True,
            },
        )
    )
    assert msg.successful_payment is not None
    assert msg.successful_payment.currency == "XTR"
    assert msg.successful_payment.total_amount == 500
    assert msg.successful_payment.is_recurring is True
    assert msg.successful_payment.is_first_recurring is True


# ---------------------------------------------------------------------------
# RefundedPayment parsing in Message
# ---------------------------------------------------------------------------


def test_refunded_payment_in_message() -> None:
    """RefundedPayment embedded in a Message."""
    msg = Message.from_dict(
        _sample_message_raw(
            3,
            refunded_payment={
                "currency": "USD",
                "total_amount": 500,
                "invoice_payload": "payload_ref",
                "telegram_payment_charge_id": "tg_charge_ref",
                "provider_payment_charge_id": "prov_charge_ref",
            },
        )
    )
    assert msg.refunded_payment is not None
    assert msg.refunded_payment.currency == "USD"
    assert msg.refunded_payment.total_amount == 500


# ---------------------------------------------------------------------------
# TransactionPartner tagged union
# ---------------------------------------------------------------------------


def test_transaction_partner_user() -> None:
    """TransactionPartnerUser parsing."""
    result = TransactionPartnerUser.from_dict({
        "type": "user",
        "user": SAMPLE_USER_RAW,
        "premium_subscription_duration": 30,
    })
    assert result is not None
    assert result.type == "user"
    assert result.user is not None
    assert result.user.id == 100
    assert result.premium_subscription_duration == 30


def test_transaction_partner_fragment() -> None:
    """TransactionPartnerFragment parsing."""
    result = TransactionPartnerFragment.from_dict({
        "type": "fragment",
    })
    assert result is not None
    assert result.type == "fragment"


def test_transaction_partner_telegram_ads() -> None:
    """TransactionPartnerTelegramAds parsing."""
    result = TransactionPartnerTelegramAds.from_dict({
        "type": "telegram_ads",
    })
    assert result is not None
    assert result.type == "telegram_ads"


def test_transaction_partner_other() -> None:
    """TransactionPartnerOther parsing."""
    result = TransactionPartnerOther.from_dict({
        "type": "other",
    })
    assert result is not None
    assert result.type == "other"


def test_star_transaction_with_partners() -> None:
    """StarTransaction with TransactionPartner source and receiver."""
    result = StarTransaction.from_dict({
        "id": "tx1",
        "amount": 100,
        "date": 1700000000,
        "source": {"type": "user", "user": SAMPLE_USER_RAW},
        "receiver": {"type": "fragment"},
        "nanostar_amount": 100000000,
    })
    assert result is not None
    assert result.id == "tx1"
    assert result.amount == 100
    assert isinstance(result.source, TransactionPartnerUser)
    assert isinstance(result.receiver, TransactionPartnerFragment)
    assert result.nanostar_amount == 100000000


# ---------------------------------------------------------------------------
# PaidMedia parsing
# ---------------------------------------------------------------------------


def test_paid_media_preview() -> None:
    result = PaidMediaPreview.from_dict({
        "type": "preview",
        "width": 100,
        "height": 100,
        "duration": 10,
    })
    assert result is not None
    assert result.type == "preview"
    assert result.width == 100
    assert result.duration == 10


def test_paid_media_photo() -> None:
    result = PaidMediaPhoto.from_dict({
        "type": "photo",
        "photo": [{"file_id": "p1", "file_unique_id": "p1u", "width": 100, "height": 100}],
    })
    assert result is not None
    assert result.type == "photo"
    assert result.photo is not None
    assert result.photo[0].file_id == "p1"


def test_paid_media_video() -> None:
    result = PaidMediaVideo.from_dict({
        "type": "video",
        "video": {"file_id": "v1", "file_unique_id": "v1u", "width": 640, "height": 480, "duration": 30},
    })
    assert result is not None
    assert result.type == "video"
    assert result.video is not None
    assert result.video.file_id == "v1"


def test_paid_media_info() -> None:
    result = PaidMediaInfo.from_dict({
        "star_count": 100,
        "paid_media": [
            {"type": "preview", "width": 100, "height": 100},
            {"type": "photo", "photo": [{"file_id": "p1", "file_unique_id": "p1u", "width": 100, "height": 100}]},
        ],
    })
    assert result is not None
    assert result.star_count == 100
    assert len(result.paid_media) == 2
    assert isinstance(result.paid_media[0], PaidMediaPreview)
    assert isinstance(result.paid_media[1], PaidMediaPhoto)


# ---------------------------------------------------------------------------
# ShippingQuery / PreCheckoutQuery parsing
# ---------------------------------------------------------------------------


def test_shipping_query_from_dict() -> None:
    result = ShippingQuery.from_dict({
        "id": "sq1",
        "from": SAMPLE_USER_RAW,
        "invoice_payload": "payload",
        "shipping_address": {
            "country_code": "US",
            "state": "CA",
            "city": "LA",
            "street_line1": "123 Main St",
            "street_line2": "Apt 1",
            "post_code": "90001",
        },
    })
    assert result is not None
    assert result.id == "sq1"
    assert result.from_ is not None
    assert result.shipping_address is not None
    assert result.shipping_address.country_code == "US"


def test_pre_checkout_query_from_dict() -> None:
    result = PreCheckoutQuery.from_dict({
        "id": "pcq1",
        "from": SAMPLE_USER_RAW,
        "currency": "USD",
        "total_amount": 1000,
        "invoice_payload": "payload",
    })
    assert result is not None
    assert result.id == "pcq1"
    assert result.currency == "USD"
    assert result.total_amount == 1000


# ---------------------------------------------------------------------------
# LabeledPrice
# ---------------------------------------------------------------------------


def test_labeled_price_roundtrip() -> None:
    lp = LabeledPrice(label="Test", amount=1000)
    d = lp.to_dict()
    assert d == {"label": "Test", "amount": 1000}


# ---------------------------------------------------------------------------
# ShippingOption
# ---------------------------------------------------------------------------


def test_shipping_option_roundtrip() -> None:
    so = ShippingOption(
        id="opt1",
        title="Standard",
        prices=[LabeledPrice(label="Shipping", amount=100)],
    )
    d = so.to_dict()
    assert d["id"] == "opt1"
    assert d["title"] == "Standard"
    assert d["prices"] == [{"label": "Shipping", "amount": 100}]
