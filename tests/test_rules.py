"""Corpus tests for assess() levels and rules."""

from __future__ import annotations

from app.rules import assess

# Synthetic only. No real names, brands, or phone numbers (AGENTS.md).


def test_empty_is_no_text():
    result = assess("")
    assert result.level == "no_text"
    assert result.findings == []


def test_whitespace_is_no_text():
    assert assess("   \n\t  ").level == "no_text"


def test_scam_many_strong_and_channels():
    message = (
        "100% sure profit today. Share your OTP and join VIP Telegram t.me/tips123 "
        "Pay registration fee only today."
    )
    result = assess(message)
    assert result.level == "many"
    rules = {f.rule for f in result.findings}
    assert "guaranteed_returns" in rules
    assert "money_or_access" in rules
    assert "private_channel" in rules
    assert any("100%" in e or "sure profit" in e.lower() for f in result.findings for e in f.evidence)


def test_hindi_guaranteed_returns():
    result = assess("इस टिप में पक्का मुनाफा है, आज ही जुड़ें।")
    rules = {f.rule for f in result.findings}
    assert "guaranteed_returns" in rules
    assert "urgency" in rules
    assert result.level == "many"  # one strong


def test_educational_warning_not_flagged():
    message = (
        "Never share your OTP with anyone. Do not join private Telegram tip groups. "
        "Ignore messages that promise guaranteed returns. This is a scam warning."
    )
    result = assess(message)
    assert result.findings == []
    assert result.level == "few"


def test_hindi_educational_warning_not_flagged():
    message = "OTP कभी न बताएं। ठगी से बचें। पक्का मुनाफा वाले संदेश न खोलें।"
    result = assess(message)
    assert result.findings == []
    assert result.level == "few"


def test_borderline_one_medium_is_few():
    result = assess("Seats are limited. Reply only today if you want details.")
    rules = {f.rule for f in result.findings}
    assert rules == {"urgency"}
    assert result.level == "few"


def test_two_medium_is_some():
    result = assess("SEBI approved operator tip. Join our private WhatsApp group.")
    rules = {f.rule for f in result.findings}
    assert "fake_authority" in rules
    assert "private_channel" in rules
    assert result.level == "some"


def test_three_medium_is_many():
    result = assess(
        "SEBI approved insider tip. Join VIP Telegram. Act now, only today left."
    )
    assert len(result.findings) >= 3
    assert result.level == "many"


def test_sebi_number_extracted_not_verified():
    result = assess("Our adviser number is INA000123456. Call for tips.")
    assert len(result.sebi_numbers) == 1
    entry = result.sebi_numbers[0]
    assert entry.number == "INA000123456"
    assert entry.verified is False
    assert entry.format_ok is True
    assert "sebi.gov.in" in entry.check_at
    assert result.sebi_claim_without_number is False


def test_sebi_claim_without_number():
    result = assess("We are SEBI registered. Message me for the secret tip.")
    assert result.sebi_claim_without_number is True
    assert result.sebi_numbers == []
    assert any(f.rule == "fake_authority" for f in result.findings)


def test_harmless_market_chat_is_few():
    result = assess("The weather is nice. Did you finish reading the newspaper?")
    assert result.level == "few"
    assert result.findings == []
