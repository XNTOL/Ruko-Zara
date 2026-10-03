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


# Patterns cover English, Hindi (Devanagari), and Hinglish (romanized).
# Prefer phrase-level matches; keep misspellings that appear in real forwards.
_RULE_SPECS: list[tuple[str, Strength, list[re.Pattern[str]]]] = [
    (
        "guaranteed_returns",
        "strong",
        [
            re.compile(r"100\s*%\s*(sure|guaranteed|profit|return|pakka)", re.I),
            re.compile(r"100\s*percent\s*(sure|guaranteed|profit|return|pakka)", re.I),
            re.compile(
                r"\bg(?:ua|au)r+a?n*t+e*d?\s+(returns?|profit|munafa)\b",
                re.I,
            ),
            re.compile(
                r"\b(?:profit|returns?|munafa)\s+g(?:ua|au)r+a?n*t+e*d?\b",
                re.I,
            ),
            re.compile(r"sure\s+(?:shot\s+)?profit", re.I),
            re.compile(r"risk[\s-]*free\s+(profit|return|munafa)", re.I),
            re.compile(r"(?:zero|no)\s*risk\s+(?:profit|return|munafa)", re.I),
            re.compile(r"\bno\s*loss\b", re.I),
            re.compile(r"double\s+(?:your\s+)?(?:money|paisa|profit)", re.I),
            re.compile(r"\b2x\s*(?:profit|returns?|money|paisa)\b", re.I),
            re.compile(r"\beasy\s+money\b", re.I),
            re.compile(r"\bfixed\s+profit\b", re.I),
            re.compile(r"\bassured\s+(?:profit|returns?|munafa)\b", re.I),
            re.compile(r"\bpakka\s*(?:munafa|profit|return|returns?)\b", re.I),
            re.compile(r"\b(?:munafa|profit)\s*pakka\b", re.I),
            re.compile(r"\bpakke?\s*returns?\b", re.I),
            re.compile(r"\bbina\s*risk\b", re.I),
            re.compile(r"\bguarantee[d]?\s*(?:wala\s*)?(?:return|profit|munafa)\b", re.I),
            re.compile(r"\bconfirmed\s+profit\b", re.I),
            re.compile(r"पक्का\s*मुना[फ़फ]ा", re.I),
            re.compile(r"मुना[फ़फ]ा\s*पक्का", re.I),
            re.compile(r"गारंटी(?:ड)?\s*(?:मुना[फ़फ]ा|रिटर्न)", re.I),
            re.compile(r"बिना\s*जोखिम\s*(?:का\s*)?मुना[फ़फ]ा", re.I),
            re.compile(r"नुकसान\s*नहीं", re.I),
            re.compile(r"पक्का\s*(?:रिटर्न|लाभ|कमाई)", re.I),
            re.compile(r"(?:दो\s*गुना|दुगना)\s*(?:पैसा|मुना[फ़फ]ा|लाभ)", re.I),
            re.compile(r"पैसा\s*दोगुना", re.I),
            re.compile(r"निश्चित\s*(?:मुना[फ़फ]ा|लाभ|रिटर्न)", re.I),
            re.compile(r"बिना\s*नुकसान", re.I),
            re.compile(r"जोखिम\s*रहित\s*(?:मुना[फ़फ]ा|लाभ|रिटर्न)?", re.I),
            re.compile(r"आसान\s*कमाई", re.I),
            re.compile(r"फिक्स्ड\s*(?:मुना[फ़फ]ा|रिटर्न|लाभ)", re.I),
        ],
    ),
    (
        "money_or_access",
        "strong",
        [
            re.compile(r"registration\s+fees?", re.I),
            re.compile(r"(?:activation|joining|security|token|kyc)\s+(?:fees?|charges?|amount|deposit)", re.I),
            re.compile(
                r"share\s+(?:your\s+)?(?:upi\s*)?(?:otp|pin|password|passcode)",
                re.I,
            ),
            re.compile(
                r"send\s+(?:your\s+)?(?:upi\s*)?(?:otp|pin|password|passcode)",
                re.I,
            ),
            re.compile(r"\botp\s*(?:bhejo|batao|bataao|do|dena|share|send)\b", re.I),
            re.compile(r"\b(?:bhejo|batao|bataao|share)\s+(?:the\s+)?otp\b", re.I),
            re.compile(
                r"\b(?:upi\s*)?pin\s*(?:bhejo|batao|bataao|do|dena|share|send)\b",
                re.I,
            ),
            re.compile(r"\botp\b", re.I),
            re.compile(r"screen[\s-]*share", re.I),
            re.compile(r"\bany[\s-]*desk\b", re.I),
            re.compile(r"\bteam[\s-]*viewer\b", re.I),
            re.compile(r"pay\s+(?:the\s+)?(?:fees?|charges?|advance)\s+first", re.I),
            re.compile(r"\bfees?\s*bharo\b", re.I),
            re.compile(r"\bpehle\s*(?:fees?|paisa|payment|advance)\b", re.I),
            re.compile(r"\baccount\s*(?:number|details?)\s*(?:bhejo|do|dena)\b", re.I),
            re.compile(r"\bdemat\s*(?:password|pin|login)\b", re.I),
            re.compile(r"शुल्क\s*(?:भरो|भेजो|दो|जमा)", re.I),
            re.compile(r"(?:रजिस्ट्रेशन|एक्टिवेशन|जॉइनिंग|सुरक्षा)\s*शुल्क", re.I),
            re.compile(r"(?:otp|ओटीपी|ओ\.?\s*टी\.?\s*पी)\s*(?:बता|भेज|दे|दीजिए|दो)", re.I),
            re.compile(r"(?:बता|भेज|दे|दीजिए|दो)\s*(?:otp|ओटीपी)", re.I),
            re.compile(r"(?:यूपीआई|upi)\s*पिन\s*(?:बता|भेज|दे|दो)", re.I),
            re.compile(r"पिन\s*(?:बता|भेज|दे|दो)", re.I),
            re.compile(r"पासवर्ड\s*(?:बता|भेज|दे|दो|शेयर)", re.I),
            re.compile(r"स्क्रीन\s*शेयर", re.I),
            re.compile(r"(?:अनीडेस्क|एनीडेस्क|anydesk)", re.I),
            re.compile(r"टीम\s*व्यूअर", re.I),
            re.compile(r"पहले\s*(?:शुल्क|पैसे?|भुगतान|एडवांस)", re.I),
            re.compile(r"(?:खाता|अकाउंट)\s*(?:नंबर|विवरण)\s*(?:भेजो|दो|बताओ)", re.I),
            re.compile(r"डीमैट\s*(?:पासवर्ड|पिन|लॉगिन)", re.I),
        ],
    ),
    (
        "urgency",
        "medium",
        [
            re.compile(r"only\s+today", re.I),
            re.compile(r"reply\s+only\s+today", re.I),
            re.compile(r"last\s+chance", re.I),
            re.compile(r"limited\s+(?:seats?|slots?|time|offer)", re.I),
            re.compile(r"hurry\s+up", re.I),
            re.compile(r"act\s+now", re.I),
            re.compile(r"don'?t\s+miss", re.I),
            re.compile(r"closing\s+soon", re.I),
            re.compile(r"offer\s+ends?\b", re.I),
            re.compile(r"\bfew\s+seats?\s+left\b", re.I),
            re.compile(r"\baaj\s*hi\b", re.I),
            re.compile(r"\bsirf\s*aaj\b", re.I),
            re.compile(r"\bjaldi(?:\s*se)?(?:\s*karo)?\b", re.I),
            re.compile(r"\babhi\s*ke\s*abhi\b", re.I),
            re.compile(r"\babhi\s*(?:join|karo|bhejo|bolo)\b", re.I),
            re.compile(r"\blast\s*(?:seat|chance|opportunity)\b", re.I),
            re.compile(r"\bseats?\s*(?:are\s+)?limited\b", re.I),
            re.compile(r"\bopportunity\s+jaa\s*rha\b", re.I),
            re.compile(r"\bmat\s*chhodna\b", re.I),
            re.compile(r"आज\s*ही", re.I),
            re.compile(r"सिर्फ\s*आज", re.I),
            re.compile(r"केवल\s*आज", re.I),
            re.compile(r"जल्दी\s*(?:करो|करें|जवाब|जुड़)", re.I),
            re.compile(r"अवसर\s*जा\s*रहा", re.I),
            re.compile(r"सीटें?\s*सीमित", re.I),
            re.compile(r"अंतिम\s*(?:अवसर|मौका|सीट)", re.I),
            re.compile(r"अभी\s*(?:जॉइन|जुड़|भेज|करो|करें)", re.I),
            re.compile(r"अभी\s*के\s*अभी", re.I),
            re.compile(r"छोड़[ोें]\s*मत", re.I),
            re.compile(r"मौका\s*हाथ\s*से\s*न\s*जाने\s*दें?", re.I),
            re.compile(r"समय\s*सीमित", re.I),
            re.compile(r"ऑफर\s*(?:समाप्त|खत्म|खत्म\s*हो)", re.I),
        ],
    ),
    (
        "fake_authority",
        "medium",
        [
            re.compile(r"sebi\s+approved", re.I),
            re.compile(r"sebi\s+registered", re.I),
            re.compile(r"sebi\s+certified", re.I),
            re.compile(r"licensed\s+by\s+sebi", re.I),
            re.compile(r"\bsebi\s*wala\b", re.I),
            re.compile(r"\bsebi\s*se\s*(?:approved|approval|registered)\b", re.I),
            re.compile(r"\bas\s+per\s+sebi\b", re.I),
            re.compile(r"\binsider\b", re.I),
            re.compile(r"\boperator\b", re.I),
            re.compile(r"rbi\s+approved", re.I),
            re.compile(r"government\s+approved", re.I),
            re.compile(r"\bgovt\.?\s*approved\b", re.I),
            re.compile(r"\bsarkari\s*(?:approved|scheme|yojana)\b", re.I),
            re.compile(r"\binsider\s*(?:tip|info|news)\b", re.I),
            re.compile(r"सेबी\s*(?:द्वारा\s*)?(?:मंजूर|अप्रूव्ड|रजिस्टर्ड|प्रमाणित)", re.I),
            re.compile(r"सेबी\s*से\s*(?:मंज़?ूरी|अप्रूवल|रजिस्टर्ड)", re.I),
            re.compile(r"सेबी\s*(?:मंज़?ूर|अनुमोदित)", re.I),
            re.compile(r"आरबीआई\s*(?:मंजूर|अप्रूव्ड)", re.I),
            re.compile(r"सरकारी\s*(?:मंज़?ूरी|योजना|स्कीम)", re.I),
            re.compile(r"इन्साइडर|इनसाइडर", re.I),
            re.compile(r"ऑपरेटर\s*(?:टिप|सलाह)?", re.I),
            re.compile(r"अंदरूनी\s*(?:जानकारी|टिप|सूचना)", re.I),
        ],
    ),
    (
        "private_channel",
        "medium",
        [
            re.compile(r"t\.me/\S+", re.I),
            re.compile(r"(?:wa\.me/|chat\.whatsapp\.com/)\S+", re.I),
            re.compile(
                r"join\s+(?:our\s+|the\s+|my\s+)?(?:vip\s+)?"
                r"(?:telegram|whatsapp|wa|group|grp|channel)",
                re.I,
            ),
            re.compile(r"join\s+(?:me\s+)?on\s+(?:telegram|whatsapp|wa)\b", re.I),
            re.compile(r"add\s+me\s+on\s+(?:telegram|whatsapp|wa)\b", re.I),
            re.compile(r"vip\s+(?:telegram|whatsapp|group|grp)", re.I),
            re.compile(r"private\s+(?:telegram|whatsapp|group|channel|grp)", re.I),
            re.compile(r"(?:telegram|whatsapp|wa)\s*(?:group|grp|channel)", re.I),
            re.compile(r"channel\s+(?:is\s+)?on\s+(?:telegram|whatsapp)\b", re.I),
            re.compile(r"\b(?:whatsapp|telegram|wa)\s*pe\s*(?:add|join|aao|ao)\b", re.I),
            re.compile(r"\bgrp\s*join\b", re.I),
            re.compile(r"download\s+(?:our\s+)?app", re.I),
            re.compile(r"\bapp\s*download(?:\s*karo)?\b", re.I),
            re.compile(r"\bdownload\s*karo\b", re.I),
            re.compile(r"टेलीग्राम", re.I),
            re.compile(r"व्हाट्स(?:अ|ऐ)प\s*(?:ग्रुप|चैनल)", re.I),
            re.compile(r"VIP\s*ग्रुप", re.I),
            re.compile(r"(?:निजी|प्राइवेट|वीआईपी|VIP)\s*(?:ग्रुप|चैनल)", re.I),
            re.compile(r"(?:ग्रुप|चैनल)\s*(?:जॉइन|जुड़)", re.I),
            re.compile(r"जॉइन\s*(?:करो|करें|कीजिए)", re.I),
            re.compile(r"(?:टेलीग्राम|व्हाट्स(?:अ|ऐ)प)\s*(?:पर|में)\s*(?:आओ|जुड़|जॉइन|ऐड)", re.I),
            re.compile(r"ऐप\s*(?:डाउनलोड|इंस्टॉल)", re.I),
            re.compile(r"डाउनलोड\s*(?:करो|करें|कीजिए)", re.I),
        ],
    ),
]

# Nearby words that mean the message warns against the matched sign.
# Hindi "न …" must not match the trailing न inside words like पिन.
_DEV_BOUND = r"(?<![\u0900-\u097F])"
_NEGATION = re.compile(
    r"(?:"
    r"\bnever\b|\bdon'?t\b|\bdo\s+not\b|\bavoid\b|\bwarn(?:s|ing)?\b|"
    r"\bscam\b|\bfraud\b|\bignore\b|\bnot\s+share\b|"
    r"\bmat\s+(?:share|bhejo|batao|bataao|do|dena|join|kholo|dena)\b|"
    r"\bkabhi\s*(?:bhi\s*)?mat\b|"
    r"\bnahi\s*(?:dena|bhejna|batana|batana)\b|"
    r"कभी\s*न[ाअ]?|"
    rf"{_DEV_BOUND}मत\s+|"
    rf"{_DEV_BOUND}नहीं\s+देना|"
    rf"{_DEV_BOUND}न\s+(?:दें|बता|खोल|भेज|जॉइन|जुड़)|"
    r"ठगी|धोखा|सावधान|बचना|बचें|चेतावनी|झूठा"
    r")",
    re.I,
)

_SEBI_NUMBER = re.compile(r"\b(IN[A-Z]{1,2}[0-9]{6,12})\b", re.I)
_SEBI_CLAIM = re.compile(
    r"(?:"
    r"sebi\s+(?:approved|registered|registration|certified|wala)|"
    r"सेबी\s*(?:द्वारा\s*|से\s*)?(?:मंज़?ूर|मंज़?ूरी|अप्रूव्ड|अप्रूवल|रजिस्टर्ड|रजिस्ट्रेशन|प्रमाणित|अनुमोदित)"
    r")",
    re.I,
)

_NEGATION_WINDOW = 56


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
