"""AI explain module: validator, limits, cache, fallback (ARCHITECTURE §6)."""

from __future__ import annotations

import httpx
import pytest

from app.explain import explain, reset_limits_for_tests, validate_summary
from app.rules import assess


class FakeResponse:
    def __init__(self, content: str, status: int = 200):
        self._content = content
        self.status_code = status

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                "error",
                request=httpx.Request("POST", "http://test"),
                response=httpx.Response(self.status_code),
            )

    def json(self) -> dict:
        return {"choices": [{"message": {"content": self._content}}]}


class FakeClient:
    def __init__(self, response: FakeResponse | None = None, error: Exception | None = None):
        self.response = response
        self.error = error
        self.calls = 0

    def post(self, *args, **kwargs):
        self.calls += 1
        if self.error:
            raise self.error
        assert self.response is not None
        return self.response

    def close(self) -> None:
        return None


@pytest.fixture(autouse=True)
def _clean_state(monkeypatch):
    reset_limits_for_tests()
    monkeypatch.setenv("AI_ENABLED", "true")
    monkeypatch.setenv("AI_API_KEY", "test-key")
    monkeypatch.setenv("AI_MODEL", "test-model")
    monkeypatch.setenv("AI_TIMEOUT_S", "4")
    monkeypatch.setenv("RATE_LIMIT_PER_MIN", "12")
    monkeypatch.setenv("DAILY_AI_CAP", "500")
    yield
    reset_limits_for_tests()


def _result():
    return assess("100% sure profit. Share your OTP. Join VIP Telegram.")


def test_validate_rejects_too_long():
    assert validate_summary("x" * 301, "en") is False


def test_validate_rejects_advice_words():
    assert validate_summary("You should buy this tip now.", "en") is False
    assert validate_summary("Please sell everything today.", "en") is False


def test_validate_rejects_safe_words():
    assert validate_summary("This message looks safe to trust.", "en") is False
    assert validate_summary("यह सुरक्षित लगता है।", "hi") is False


def test_validate_rejects_url_and_phone():
    assert validate_summary("See https://example.com for help.", "en") is False
    assert validate_summary("Call 9876543210 for help.", "en") is False


def test_validate_hindi_needs_devanagari():
    assert validate_summary("This is mostly English words here.", "hi") is False
    assert (
        validate_summary("संदेश में पक्के मुनाफ़े जैसे संकेत दिखे। सावधान रहें।", "hi")
        is True
    )


def test_validate_accepts_plain_english():
    text = "The message promises sure profit and asks for an OTP. Be careful."
    assert validate_summary(text, "en") is True


def test_explain_success_returns_text():
    client = FakeClient(
        FakeResponse("The message promises sure profit and asks for secrecy.")
    )
    out = explain("masked tip", _result(), "en", http_client=client, client_ip="1.1.1.1")
    assert out is not None
    assert "sure profit" in out
    assert client.calls == 1


def test_explain_timeout_returns_none():
    client = FakeClient(error=httpx.TimeoutException("timeout"))
    out = explain("masked tip", _result(), "en", http_client=client, client_ip="1.1.1.1")
    assert out is None
    assert client.calls == 1


def test_explain_rejects_invalid_model_output():
    client = FakeClient(FakeResponse("This tip is safe. You should buy now."))
    out = explain("masked tip", _result(), "en", http_client=client, client_ip="1.1.1.1")
    assert out is None


def test_ai_disabled_makes_no_http_call(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "false")
    client = FakeClient(FakeResponse("Should not be used"))
    out = explain("masked tip", _result(), "en", http_client=client, client_ip="1.1.1.1")
    assert out is None
    assert client.calls == 0


def test_explain_uses_cache(monkeypatch):
    client = FakeClient(
        FakeResponse("The message shows pressure and private-group patterns.")
    )
    a = explain("same masked", _result(), "en", http_client=client, client_ip="1.1.1.1")
    b = explain("same masked", _result(), "en", http_client=client, client_ip="1.1.1.1")
    assert a == b
    assert client.calls == 1


def test_check_works_with_ai_off(monkeypatch):
    monkeypatch.setenv("AI_ENABLED", "false")
    from fastapi.testclient import TestClient

    from app.main import EXAMPLES, app

    client = TestClient(app)
    response = client.post(
        "/check",
        data={"message": EXAMPLES["scam"], "lang": "en"},
    )
    assert response.status_code == 200
    assert 'data-level="many"' in response.text
    assert 'data-ai="1"' not in response.text
