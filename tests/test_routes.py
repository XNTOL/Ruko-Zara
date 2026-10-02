"""Route tests: tracer bullet + T3 (FR-3, FR-6, FR-11)."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.content import CAVEAT, LEVELS, LINKS, TEXT
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
    assert "जाँचें" in response.text
    assert "/about?lang=hi" in response.text


def test_index_example_scam_fills_textarea():
    response = client.get("/?lang=en&example=scam")
    assert response.status_code == 200
    assert "100% sure profit" in response.text
    assert "example=edu" in response.text  # cycles to next


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
    assert CAVEAT["en"] in html
    assert 'data-caveat="1"' in html
    assert "Set-Cookie" not in response.headers


def test_check_scam_hindi_level_title():
    response = client.post("/check", data={"message": SCAM, "lang": "hi"})
    assert response.status_code == 200
    assert LEVELS["many"]["hi"] in response.text
    assert TEXT["guaranteed_returns"]["title"]["hi"] in response.text
    assert CAVEAT["hi"] in response.text


def test_fr6_sebi_number_block():
    message = "Contact our adviser INA000123456 for the tip group."
    response = client.post("/check", data={"message": message, "lang": "en"})
    assert response.status_code == 200
    html = response.text
    assert 'data-sebi="1"' in html
    assert "INA000123456" in html
    assert "cannot verify" in html
    assert LINKS["sebi_check"] in html


def test_fr6_sebi_claim_without_number():
    message = "We are SEBI registered. Message for the secret tip."
    response = client.post("/check", data={"message": message, "lang": "en"})
    assert response.status_code == 200
    html = response.text
    assert 'data-sebi="1"' in html
    assert "claims SEBI registration but gives no number" in html


def test_about_page_fr11():
    response = client.get("/about?lang=en")
    assert response.status_code == 200
    html = response.text
    assert "How it works" in html
    assert "What is stored" in html
    assert "Nothing" in html
    assert "Honest limits" in html
    assert "does not know who sent the message" in html
    assert "cannot verify a SEBI number" in html


def test_about_page_hindi():
    response = client.get("/about?lang=hi")
    assert response.status_code == 200
    assert "इस ऐप के बारे में" in response.text


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


def test_result_has_no_full_message_echo():
    marker = "UNIQUE_MARKER_XYZ_SHOULD_NOT_ECHO"
    message = f"100% sure profit join VIP Telegram. {marker}"
    response = client.post("/check", data={"message": message, "lang": "en"})
    assert response.status_code == 200
    assert marker not in response.text
