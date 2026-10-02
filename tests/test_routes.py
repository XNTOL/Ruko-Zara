"""Route tests for the T2 tracer bullet."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.content import LEVELS, TEXT
from app.main import EXAMPLES, app

client = TestClient(app)

SCAM = EXAMPLES["scam"]


def test_healthz_ok():
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_index_renders_form():
    response = client.get("/")
    assert response.status_code == 200
    assert 'name="message"' in response.text
    assert "जाँचें" in response.text or "Check" in response.text


def test_index_example_scam_fills_textarea():
    response = client.get("/?lang=en&example=scam")
    assert response.status_code == 200
    assert "100% sure profit" in response.text


def test_check_scam_shows_many_and_reasons():
    response = client.post("/check", data={"message": SCAM, "lang": "en"})
    assert response.status_code == 200
    html = response.text
    assert LEVELS["many"]["en"] in html
    assert 'data-level="many"' in html
    assert TEXT["guaranteed_returns"]["title"]["en"] in html
    assert TEXT["money_or_access"]["title"]["en"] in html
    assert TEXT["private_channel"]["title"]["en"] in html
    assert TEXT["guaranteed_returns"]["why"]["en"] in html
    assert "<mark>" in html


def test_check_scam_hindi_level_title():
    response = client.post("/check", data={"message": SCAM, "lang": "hi"})
    assert response.status_code == 200
    assert LEVELS["many"]["hi"] in response.text
    assert TEXT["guaranteed_returns"]["title"]["hi"] in response.text


def test_empty_message_returns_422_form():
    response = client.post("/check", data={"message": "hi", "lang": "en"})
    assert response.status_code == 422
    assert "Paste a message first" in response.text
    assert 'name="message"' in response.text


def test_long_message_returns_422():
    response = client.post(
        "/check",
        data={"message": "x" * 2001, "lang": "en"},
    )
    assert response.status_code == 422
    assert "too long" in response.text.lower()
