"""Route tests: tracer bullet + T3 (FR-3, FR-6, FR-11) + T4 CSS."""

from __future__ import annotations

from pathlib import Path

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


def test_css_linked_and_under_budget():
    css_path = Path(__file__).resolve().parents[1] / "app" / "static" / "app.css"
    size = css_path.stat().st_size
    assert size <= 12 * 1024, f"app.css is {size} bytes"
    home = client.get("/")
    assert 'href="/static/app.css"' in home.text
    css = client.get("/static/app.css")
    assert css.status_code == 200
    assert b"--primary" in css.content
    assert b"--many-bg" in css.content


def test_language_switch_marks_active():
    hi = client.get("/?lang=hi")
    assert 'aria-current="true"' in hi.text
    assert "lang-switch" in hi.text
    # Active Hindi link appears before EN in nav
    assert hi.text.index('aria-current="true"') < hi.text.index(">EN<")

    en = client.get("/?lang=en")
    assert 'href="/?lang=en"' in en.text or 'href="/?lang=en' in en.text
    # EN is current
    assert en.text.count('aria-current="true"') >= 1


def test_result_level_card_has_icon_and_no_green():
    response = client.post("/check", data={"message": SCAM, "lang": "en"})
    html = response.text
    assert "level--many" in html
    assert "level__icon" in html
    assert "<svg" in html
    css = client.get("/static/app.css").text.lower()
    assert "green" not in css
    assert "#22c55e" not in css
    assert "checkmark" not in css


def test_js_listen_wired_and_under_budget():
    js_path = Path(__file__).resolve().parents[1] / "app" / "static" / "app.js"
    size = js_path.stat().st_size
    assert size <= 8 * 1024, f"app.js is {size} bytes"
    home = client.get("/")
    assert 'src="/static/app.js"' in home.text
    assert 'data-loading=' in home.text
    js = client.get("/static/app.js")
    assert js.status_code == 200
    assert b"speechSynthesis" in js.content
    assert b"voice-none" in js.content
    assert b"applyResultLang" in js.content or b"data-set-lang" in js.content

    result = client.post("/check", data={"message": SCAM, "lang": "hi"})
    html = result.text
    assert 'id="btn-listen"' in html
    assert "data-speak=" in html
    assert "data-label-listen=" in html
    assert "data-label-stop=" in html
    assert 'id="voice-none"' in html
    assert "सुनें" in html
    assert 'id="result-i18n"' in html
    assert 'data-set-lang="hi"' in html
    assert 'data-set-lang="en"' in html
    # In-place switch: no home redirect links for language on result
    assert 'href="/?lang=hi"' not in html.split("lang-switch")[1].split("</nav>")[0]
    assert "Many warning signs found" in html  # en pack embedded
    assert LEVELS["many"]["hi"] in html


def test_pause_and_report_on_all_levels():
    """T6: pause step + reporting list at every level."""
    cases = [
        (SCAM, "many"),
        (
            "SEBI approved operator tip. Join our private WhatsApp group.",
            "some",
        ),
        ("Seats are limited. Reply only today if you want details.", "few"),
    ]
    for message, level in cases:
        response = client.post("/check", data={"message": message, "lang": "en"})
        assert response.status_code == 200, level
        html = response.text
        assert f'data-level="{level}"' in html
        assert 'data-pause="1"' in html
        assert 'data-report="1"' in html
        assert "Do not send money" in html
        assert "tel:1930" in html
        assert "cybercrime.gov.in" in html or LINKS["cybercrime"] in html
        assert "scores.sebi.gov.in" in html or LINKS["scores"] in html
        assert "bank or UPI" in html


def test_warning_card_has_rule_titles_only():
    """T8: card holds rule titles, never the original message."""
    marker = "SECRET_ORIGINAL_MESSAGE_XYZ"
    message = f"100% sure profit. Join VIP Telegram. {marker}"
    response = client.post("/check", data={"message": message, "lang": "en"})
    assert response.status_code == 200
    html = response.text
    assert 'data-card="1"' in html
    assert 'id="card-text"' in html
    assert 'id="btn-copy"' in html
    assert "Copy warning" in html
    assert "Warning for your family group" in html
    assert TEXT["guaranteed_returns"]["title"]["en"] in html
    assert TEXT["private_channel"]["title"]["en"] in html
    assert marker not in html
    assert "Ruko Zara!" in html
    # Copy helper present in JS
    js = client.get("/static/app.js").text
    assert "btn-copy" in js
    assert "clipboard" in js
