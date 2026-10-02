"""Corpus tests for assess() levels and rules."""

from __future__ import annotations

import pytest

from app.rules import assess

# Synthetic only. No real names, brands, or phone numbers (AGENTS.md).
# At least 20 messages across Hindi, English, and Hinglish (PRODUCT_SPEC §10).

CORPUS: list[tuple[str, str, str]] = [
    # kind, lang-ish label, text
    (
        "scam",
        "en",
        "100% sure profit today. Share your OTP and join VIP Telegram t.me/tips123 "
        "Pay registration fee only today.",
    ),
    ("scam", "hi", "इस टिप में पक्का मुनाफा है, आज ही जुड़ें और OTP भेजो।"),
    (
        "scam",
        "hinglish",
        "Bhai guaranteed returns milega. SEBI approved operator. Download app abhi.",
    ),
    (
        "scam",
        "en",
        "Double your money risk-free. Screen-share on AnyDesk and pay fees first.",
    ),
    (
        "scam",
        "hi",
        "गारंटीड मुनाफा! VIP ग्रुप जॉइन करो। शुल्क भरो और स्क्रीन शेयर करो।",
    ),
    (
        "scam",
        "en",
        "Insider tip from SEBI certified desk. Limited seats. Act now.",
    ),
    (
        "scam",
        "hinglish",
        "Only today last chance. Join private WhatsApp group for sure profit.",
    ),
    (
        "edu",
        "en",
        "Never share your OTP with anyone. Do not join private Telegram tip groups. "
        "Ignore messages that promise guaranteed returns. This is a scam warning.",
    ),
    (
        "edu",
        "hi",
        "OTP कभी न बताएं। ठगी से बचें। पक्का मुनाफा वाले संदेश न खोलें।",
    ),
    (
        "edu",
        "hinglish",
        "Kabhi bhi OTP mat share karo. Private tip Telegram ignore karo. Scam warning.",
    ),
    (
        "edu",
        "en",
        "Do not pay a registration fee for tips. Avoid screen-share apps. Warn family.",
    ),
    (
        "edu",
        "hi",
        "रजिस्ट्रेशन शुल्क मत दो। स्क्रीन शेयर से बचें। यह ठगी की चेतावनी है।",
    ),
    (
        "border",
        "en",
        "Seats are limited. Reply only today if you want details.",
    ),
    ("border", "hi", "सीटें सीमित हैं। आज ही जवाब दें।"),
    (
        "border",
        "hinglish",
        "Limited time offer hai, hurry up if interested.",
    ),
    (
        "border",
        "en",
        "Our channel is on Telegram if you want market notes.",
    ),
    (
        "border",
        "en",
        "Someone said the tip looks SEBI approved, no number given.",
    ),
    ("clean", "en", "The weather is nice. Did you finish reading the newspaper?"),
    ("clean", "hi", "आज मौसम अच्छा है। चाय पी लो।"),
    (
        "clean",
        "hinglish",
        "Kal family dinner hai. Time pe ghar aana.",
    ),
    ("clean", "en", "Please bring milk and sugar from the shop."),
    (
        "scam",
        "en",
        "Government approved trading desk. Download our app. Share OTP to activate.",
    ),
]


def test_corpus_has_at_least_20_synthetic_messages():
    assert len(CORPUS) >= 20
    kinds = {row[0] for row in CORPUS}
    assert {"scam", "edu", "border", "clean"} <= kinds
    langs = {row[1] for row in CORPUS}
    assert {"en", "hi", "hinglish"} <= langs


@pytest.mark.parametrize("kind,lang,text", CORPUS)
def test_corpus_messages_are_assessable(kind: str, lang: str, text: str):
    result = assess(text)
    assert result.level in {"many", "some", "few", "no_text"}
    if kind == "edu":
        assert result.findings == []
        assert result.level == "few"
    if kind == "clean":
        assert result.findings == []
        assert result.level == "few"
    if kind == "scam":
        assert result.level in {"many", "some"}
        assert result.findings


def test_empty_is_no_text():
    result = assess("")
    assert result.level == "no_text"
    assert result.findings == []


def test_whitespace_is_no_text():
    assert assess("   \n\t  ").level == "no_text"


def test_scam_many_strong_and_channels():
    message = CORPUS[0][2]
    result = assess(message)
    assert result.level == "many"
    rules = {f.rule for f in result.findings}
    assert "guaranteed_returns" in rules
    assert "money_or_access" in rules
    assert "private_channel" in rules


def test_hindi_guaranteed_returns():
    result = assess("इस टिप में पक्का मुनाफा है, आज ही जुड़ें।")
    rules = {f.rule for f in result.findings}
    assert "guaranteed_returns" in rules
    assert "urgency" in rules
    assert result.level == "many"


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
