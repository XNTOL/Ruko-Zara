"""T10: page-weight and accessibility budgets (ARCHITECTURE §8, UIUX §8)."""

from __future__ import annotations

import re
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import EXAMPLES, app

client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "app" / "static" / "app.css").read_text(encoding="utf-8")
JS = (ROOT / "app" / "static" / "app.js").read_text(encoding="utf-8")


def test_asset_byte_budgets():
    css_bytes = (ROOT / "app" / "static" / "app.css").stat().st_size
    js_bytes = (ROOT / "app" / "static" / "app.js").stat().st_size
    assert css_bytes <= 12 * 1024, f"app.css {css_bytes}"
    assert js_bytes <= 8 * 1024, f"app.js {js_bytes}"


def test_first_load_under_100kb():
    home = client.get("/")
    css = client.get("/static/app.css")
    js = client.get("/static/app.js")
    total = len(home.content) + len(css.content) + len(js.content)
    assert home.status_code == 200
    assert css.status_code == 200
    assert js.status_code == 200
    assert total <= 100 * 1024, f"first load {total} bytes"


def test_css_has_required_tokens_and_no_green():
    for token in (
        "--bg:",
        "--text:",
        "--primary:",
        "--many-bg:",
        "--some-bg:",
        "--few-bg:",
        "--tap:",
    ):
        assert token in CSS
    lower = CSS.lower()
    assert "green" not in lower
    assert "#22c55e" not in lower
    assert "checkmark" not in lower
    assert re.search(r"font:\s*20px", CSS) or "font-size: 20px" in CSS
    assert "outline" in CSS
    assert "prefers-reduced-motion" in CSS
    assert "overflow-x" in CSS


def test_css_tap_targets_use_56px():
    assert "--tap: 56px" in CSS or "--tap:56px" in CSS
    assert "min-height: var(--tap)" in CSS
    # Language switch and footer links must also meet the budget.
    assert "min-height: var(--tap)" in CSS
    assert ".lang-switch" in CSS


def test_home_hindi_default_and_landmarks():
    response = client.get("/")
    html = response.text
    assert 'lang="hi"' in html
    assert 'id="main"' in html
    assert 'href="#main"' in html
    assert 'href="/static/app.css"' in html


def test_result_accessible_structure():
    response = client.post(
        "/check",
        data={"message": EXAMPLES["scam"], "lang": "hi"},
    )
    html = response.text
    assert response.status_code == 200
    assert "level__icon" in html
    assert "<svg" in html
    assert 'data-caveat="1"' in html
    assert 'data-pause="1"' in html
    assert 'data-report="1"' in html
    assert "#22c55e" not in html.lower()


def test_js_off_still_gets_full_result():
    """Core journey works without depending on JS for the POST result."""
    response = client.post(
        "/check",
        data={"message": EXAMPLES["scam"], "lang": "en"},
    )
    assert response.status_code == 200
    assert "Many warning signs" in response.text
    assert "Do not send money" in response.text
    assert "Copy warning" in response.text
