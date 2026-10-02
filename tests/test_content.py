"""T1: content keys, bilingual parity, guardrail wording, URL allowlist."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

from app import content
from app.content import (
    ABOUT_LIMITS,
    ALLOWED_URLS,
    CAVEAT,
    LEVELS,
    LINKS,
    RULE_IDS,
    STRINGS,
    TEXT,
    UI_KEYS,
)

# Words that must never appear in fixed product copy (G1 / G4).
_FORBIDDEN = re.compile(
    r"(?i)(?<!\w)(?:safe|सुरक्षित|genuine|असली|legit|"
    r"buy|sell|hold|target|invest\s+in|खरीद|बेच|टारगेट)(?!\w)"
)

_URL_IN_TEXT = re.compile(r"https?://[^\s\"'<>]+")


def test_ui_keys_match_across_languages():
    assert set(STRINGS["hi"]) == set(STRINGS["en"]) == UI_KEYS


def test_every_ui_key_has_nonempty_hi_and_en():
    for key in UI_KEYS:
        for lang in ("hi", "en"):
            value = STRINGS[lang][key]
            assert isinstance(value, str) and value.strip(), f"{lang}.{key}"


def test_levels_and_caveat_present():
    for level in ("many", "some", "few", "no_text"):
        assert level in LEVELS
        for lang in ("hi", "en"):
            assert LEVELS[level][lang].strip()
    for lang in ("hi", "en"):
        assert CAVEAT[lang].strip()


def test_rule_text_covers_all_rule_ids():
    assert RULE_IDS == {
        "guaranteed_returns",
        "money_or_access",
        "urgency",
        "fake_authority",
        "private_channel",
    }
    for rule_id in RULE_IDS:
        for field in ("title", "why"):
            for lang in ("hi", "en"):
                assert TEXT[rule_id][field][lang].strip(), f"{rule_id}.{field}.{lang}"


def test_few_level_never_says_safe():
    for lang in ("hi", "en"):
        title = LEVELS["few"][lang].lower()
        assert "safe" not in title
        assert "सुरक्षित" not in LEVELS["few"][lang]


def test_no_forbidden_advice_or_safe_words_in_copy():
    blobs: list[str] = []
    for lang in ("hi", "en"):
        blobs.extend(STRINGS[lang].values())
        blobs.append(CAVEAT[lang])
        blobs.extend(ABOUT_LIMITS[lang])
        for level in LEVELS.values():
            blobs.append(level[lang])
        for rule in TEXT.values():
            blobs.append(rule["title"][lang])
            blobs.append(rule["why"][lang])
    for blob in blobs:
        match = _FORBIDDEN.search(blob)
        assert match is None, f"forbidden term {match.group(0)!r} in {blob!r}"


def test_links_are_official_allowlist_only():
    assert LINKS["helpline"] == "tel:1930"
    for key, url in LINKS.items():
        assert url in ALLOWED_URLS, key
    for url in ALLOWED_URLS:
        if url.startswith("tel:"):
            continue
        assert "sebi.gov.in" in url or "cybercrime.gov.in" in url or "scores.sebi.gov.in" in url


def test_no_unexpected_http_urls_in_strings():
    for lang in ("hi", "en"):
        for key, value in STRINGS[lang].items():
            for url in _URL_IN_TEXT.findall(value):
                assert url in ALLOWED_URLS, f"{lang}.{key}: {url}"


@pytest.mark.xfail(reason="Hindi native review pending; # REVIEW tags remain by design", strict=False)
def test_no_review_tags_remain():
    source = Path(content.__file__).read_text(encoding="utf-8")
    assert "# REVIEW" not in source
