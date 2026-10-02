"""Patterns and assess(). Truth for scoring. No user-facing copy here."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from app.content import LINKS

Strength = str  # "strong" | "medium"
Level = str  # "many" | "some" | "few" | "no_text"


@dataclass(frozen=True)
class Finding:
    rule: str
    strength: Strength
    evidence: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class SebiNumber:
    number: str
    category_hint: str
    format_ok: bool
    verified: bool = False
    check_at: str = LINKS["sebi_check"]


@dataclass(frozen=True)
class Result:
    level: Level
    findings: list[Finding] = field(default_factory=list)
    sebi_numbers: list[SebiNumber] = field(default_factory=list)
    sebi_claim_without_number: bool = False


# Each rule: (rule_id, strength, compiled patterns).
_RULE_SPECS: list[tuple[str, Strength, list[re.Pattern[str]]]] = [
    (
        "guaranteed_returns",
        "strong",
        [
            re.compile(r"100\s*%\s*(sure|guaranteed|profit|return)", re.I),
            re.compile(r"guaranteed\s+(returns?|profit)", re.I),
            re.compile(r"sure\s+profit", re.I),
            re.compile(r"risk[\s-]*free\s+(profit|return)", re.I),
            re.compile(r"double\s+your\s+money", re.I),
            re.compile(r"पक्का\s*मुना[फ़फ]ा", re.I),
            re.compile(r"गारंटी(?:ड)?\s*(?:मुना[फ़फ]ा|रिटर्न)", re.I),
            re.compile(r"बिना\s*जोखिम\s*(?:का\s*)?मुना[फ़फ]ा", re.I),
        ],
    ),
    (
        "money_or_access",
        "strong",
        [
            re.compile(r"registration\s+fee", re.I),
            re.compile(r"share\s+your\s+otp", re.I),
            re.compile(r"send\s+(?:your\s+)?otp", re.I),
            re.compile(r"\botp\b", re.I),
            re.compile(r"screen[\s-]*share", re.I),
            re.compile(r"\banydesk\b", re.I),
            re.compile(r"\bteamviewer\b", re.I),
            re.compile(r"pay\s+(?:the\s+)?(?:fees?|charges?)\s+first", re.I),
            re.compile(r"शुल्क\s*(?:भरो|भेजो|दो)", re.I),
            re.compile(r"otp\s*(?:बता|भेज|दे)", re.I),
            re.compile(r"स्क्रीन\s*शेयर", re.I),
        ],
    ),
    (
        "urgency",
        "medium",
        [
            re.compile(r"only\s+today", re.I),
            re.compile(r"last\s+chance", re.I),
            re.compile(r"limited\s+(?:seats?|slots?|time)", re.I),
            re.compile(r"hurry\s+up", re.I),
            re.compile(r"act\s+now", re.I),
            re.compile(r"आज\s*ही", re.I),
            re.compile(r"सिर्फ\s*आज", re.I),
            re.compile(r"जल्दी\s*(?:करो|करें)", re.I),
            re.compile(r"अवसर\s*जा\s*रहा", re.I),
        ],
    ),
    (
        "fake_authority",
        "medium",
        [
            re.compile(r"sebi\s+approved", re.I),
            re.compile(r"sebi\s+registered", re.I),
            re.compile(r"sebi\s+certified", re.I),
            re.compile(r"\binsider\b", re.I),
            re.compile(r"\boperator\b", re.I),
            re.compile(r"rbi\s+approved", re.I),
            re.compile(r"government\s+approved", re.I),
            re.compile(r"सेबी\s*(?:द्वारा\s*)?(?:मंजूर|अप्रूव्ड|रजिस्टर्ड)", re.I),
            re.compile(r"सरकारी\s*मंज़?ूरी", re.I),
            re.compile(r"इन्साइडर", re.I),
        ],
    ),
    (
        "private_channel",
        "medium",
        [
            re.compile(r"t\.me/\S+", re.I),
            re.compile(r"join\s+(?:our\s+)?(?:vip\s+)?(?:telegram|whatsapp)", re.I),
            re.compile(r"vip\s+(?:telegram|whatsapp|group)", re.I),
            re.compile(r"private\s+(?:telegram|whatsapp|group|channel)", re.I),
            re.compile(r"download\s+(?:our\s+)?app", re.I),
            re.compile(r"टेलीग्राम", re.I),
            re.compile(r"व्हाट्स(?:अ|ऐ)प\s*ग्रुप", re.I),
            re.compile(r"VIP\s*ग्रुप", re.I),
            re.compile(r"ऐप\s*डाउनलोड", re.I),
        ],
    ),
]

# Nearby words that mean the message warns against the matched sign.
_NEGATION = re.compile(
    r"(?:"
    r"\bnever\b|\bdon'?t\b|\bdo\s+not\b|\bavoid\b|\bwarn(?:s|ing)?\b|"
    r"\bscam\b|\bfraud\b|\bignore\b|\bnot\s+share\b|"
    r"कभी\s*न[ाअ]?|मत\s+|न\s+दें|न\s+बता|नहीं\s+देना|"
    r"न\s+खोल|ठगी|सावधान|बचना|बचें"
    r")",
    re.I,
)

_SEBI_NUMBER = re.compile(r"\b(IN[A-Z]{1,2}[0-9]{6,12})\b", re.I)
_SEBI_CLAIM = re.compile(
    r"(?:"
    r"sebi\s+(?:approved|registered|registration|certified)|"
    r"सेबी\s*(?:द्वारा\s*)?(?:मंजूर|अप्रूव्ड|रजिस्टर्ड|रजिस्ट्रेशन)"
    r")",
    re.I,
)

_NEGATION_WINDOW = 48


def _is_warning_context(text: str, start: int, end: int) -> bool:
    left = max(0, start - _NEGATION_WINDOW)
    right = min(len(text), end + _NEGATION_WINDOW)
    return bool(_NEGATION.search(text[left:right]))


def _category_hint(number: str) -> str:
    prefix = number[:3].upper()
    hints = {
        "INA": "investment_adviser",
        "INB": "broker",
        "INH": "research_analyst",
        "INP": "portfolio_manager",
        "INS": "other",
    }
    return hints.get(prefix, "intermediary")


def _format_ok(number: str) -> bool:
    return bool(re.fullmatch(r"IN[A-Z]{1,2}[0-9]{6,12}", number, re.I))


def _level_for(findings: list[Finding]) -> Level:
    if not findings:
        return "few"
    strong = sum(1 for f in findings if f.strength == "strong")
    total = len(findings)
    if strong >= 1 or total >= 3:
        return "many"
    if total == 2:
        return "some"
    return "few"


def assess(text: str) -> Result:
    """Score a pasted message. Runs on the original text (not masked)."""
    if text is None or not str(text).strip():
        return Result(level="no_text")

    body = str(text)
    findings: list[Finding] = []

    for rule_id, strength, patterns in _RULE_SPECS:
        evidence: list[str] = []
        for pattern in patterns:
            for match in pattern.finditer(body):
                if _is_warning_context(body, match.start(), match.end()):
                    continue
                snippet = match.group(0).strip()
                if snippet and snippet not in evidence:
                    evidence.append(snippet)
        if evidence:
            findings.append(Finding(rule=rule_id, strength=strength, evidence=evidence))

    sebi_numbers: list[SebiNumber] = []
    seen: set[str] = set()
    for match in _SEBI_NUMBER.finditer(body):
        number = match.group(1).upper()
        if number in seen:
            continue
        seen.add(number)
        sebi_numbers.append(
            SebiNumber(
                number=number,
                category_hint=_category_hint(number),
                format_ok=_format_ok(number),
                verified=False,
                check_at=LINKS["sebi_check"],
            )
        )

    claim = bool(_SEBI_CLAIM.search(body)) and not sebi_numbers

    return Result(
        level=_level_for(findings),
        findings=findings,
        sebi_numbers=sebi_numbers,
        sebi_claim_without_number=claim,
    )
