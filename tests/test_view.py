"""T3: view-model includes FR-3 / FR-6 fields."""

from __future__ import annotations

from app.rules import assess
from app.view import build_about, build_view


def test_build_view_reasons_and_caveat():
    result = assess(
        "100% sure profit. Share your OTP. Join VIP Telegram t.me/x only today."
    )
    vm = build_view(result, summary=None, lang="en")
    assert vm["level"] == "many"
    assert vm["level_title"]
    assert vm["reasons"]
    assert vm["caveat"]
    assert vm["summary"] is None
    assert "sure profit" in vm["speak_text"].lower() or "Promise" in vm["speak_text"]


def test_build_view_sebi_number():
    result = assess("Our number is INA000123456.")
    vm = build_view(result, None, "en")
    assert vm["sebi"]["show"] is True
    assert vm["sebi"]["numbers"][0]["number"] == "INA000123456"


def test_build_about_limits():
    vm = build_about("en")
    assert len(vm["limits"]) >= 6
    assert any("SEBI number" in line for line in vm["limits"])
