"""Build the template view-model from an assess() Result."""

from __future__ import annotations

from app.content import ABOUT_LIMITS, CAVEAT, LEVELS, LINKS, STRINGS, TEXT
from app.rules import Result


def _code(lang: str) -> str:
    return "en" if lang == "en" else "hi"


def _strings(lang: str) -> dict[str, str]:
    return STRINGS[_code(lang)]


def _reasons(result: Result, lang: str) -> list[dict[str, object]]:
    code = _code(lang)
    reasons: list[dict[str, object]] = []
    for finding in result.findings:
        copy = TEXT[finding.rule]
        reasons.append(
            {
                "rule": finding.rule,
                "title": copy["title"][code],
                "why": copy["why"][code],
                "evidence": list(finding.evidence),
            }
        )
    return reasons


def _card_text(result: Result, lang: str) -> str:
    code = _code(lang)
    strings = _strings(lang)
    titles = [TEXT[f.rule]["title"][code] for f in result.findings]
    joined = ", ".join(titles) if titles else "—"
    return strings["card_template"].format(titles=joined)


def _speak_text(level_title: str, reasons: list[dict[str, object]], lang: str) -> str:
    strings = _strings(lang)
    parts = [level_title]
    for reason in reasons:
        parts.append(str(reason["title"]))
    parts.extend([strings["pause_1"], strings["pause_2"], strings["pause_3"]])
    return " ".join(parts)


def _pause(lang: str) -> dict[str, object]:
    strings = _strings(lang)
    return {
        "title": strings["pause_title"],
        "steps": [strings["pause_1"], strings["pause_2"], strings["pause_3"]],
        "report_title": strings["report_title"],
        "report_bank_hint": strings["report_bank_hint"],
        "report_call_hint": strings["report_call_hint"],
        "report": [
            {
                "key": "1930",
                "kind": "call",
                "text": strings["report_1930"],
                "href": LINKS["helpline"],
            },
            {
                "key": "portal",
                "kind": "web",
                "text": strings["report_portal"],
                "href": LINKS["cybercrime"],
            },
            {
                "key": "scores",
                "kind": "web",
                "text": strings["report_scores"],
                "href": LINKS["scores"],
            },
            {
                "key": "bank",
                "kind": "note",
                "text": strings["report_bank"],
                "href": None,
            },
        ],
    }


def _sebi(result: Result, lang: str) -> dict[str, object]:
    strings = _strings(lang)
    numbers = []
    for entry in result.sebi_numbers:
        numbers.append(
            {
                "number": entry.number,
                "text": strings["sebi_found"].format(number=entry.number),
                "check_at": entry.check_at,
                "btn": strings["btn_sebi"],
            }
        )
    return {
        "numbers": numbers,
        "claim_without_number": result.sebi_claim_without_number,
        "claim_text": strings["sebi_claim_no_number"],
        "show": bool(numbers) or result.sebi_claim_without_number,
    }


def _locale_pack(result: Result, summary: str | None, lang: str) -> dict[str, object]:
    """One language's strings for the result page (no original message)."""
    lang = _code(lang)
    strings = _strings(lang)
    reasons = _reasons(result, lang)
    level_title = LEVELS[result.level][lang]
    pause = _pause(lang)
    sebi = _sebi(result, lang)
    return {
        "level_title": level_title,
        "reasons": [
            {"rule": r["rule"], "title": r["title"], "why": r["why"]} for r in reasons
        ],
        "section_none": strings["section_none"],
        "caveat": CAVEAT[lang],
        "summary": summary,
        "sebi": sebi,
        "pause": pause,
        "card_text": _card_text(result, lang),
        "speak_text": _speak_text(level_title, reasons, lang),
        "t": {
            "app_title": strings["app_title"],
            "section_reasons": strings["section_reasons"],
            "matched": strings["matched"],
            "ai_label": strings["ai_label"],
            "btn_listen": strings["btn_listen"],
            "btn_stop": strings["btn_stop"],
            "voice_none": strings["voice_none"],
            "btn_again": strings["btn_again"],
            "about_link": strings["about_link"],
            "footer": strings["footer"],
            "lang_hi": strings["lang_hi"],
            "lang_en": strings["lang_en"],
            "btn_sebi": strings["btn_sebi"],
            "card_title": strings["card_title"],
            "btn_copy": strings["btn_copy"],
            "copied": strings["copied"],
        },
    }


def build_view(
    result: Result,
    summary: str | None,
    lang: str,
) -> dict[str, object]:
    """Return the dict passed to result.html (ARCHITECTURE §3)."""
    lang = _code(lang)
    pack = _locale_pack(result, summary, lang)
    strings = _strings(lang)

    return {
        "lang": lang,
        "level": result.level,
        "level_title": pack["level_title"],
        "reasons": _reasons(result, lang),
        "caveat": pack["caveat"],
        "summary": summary,
        "sebi": pack["sebi"],
        "pause": pack["pause"],
        "card_text": pack["card_text"],
        "speak_text": pack["speak_text"],
        "t": strings,
        "other_lang": "en" if lang == "hi" else "hi",
        "page_kind": "result",
        # Summary only in the language it was written for (AI is one lang).
        "i18n": {
            "hi": _locale_pack(result, summary if lang == "hi" else None, "hi"),
            "en": _locale_pack(result, summary if lang == "en" else None, "en"),
        },
    }


def build_about(lang: str) -> dict[str, object]:
    lang = _code(lang)
    strings = _strings(lang)
    return {
        "lang": lang,
        "t": strings,
        "limits": ABOUT_LIMITS[lang],
        "other_lang": "en" if lang == "hi" else "hi",
        "page_kind": "about",
        "page_title": strings["about_title"],
    }


def build_index(
    lang: str,
    *,
    message: str = "",
    error: str | None = None,
    example: str | None = None,
    next_example: str = "scam",
) -> dict[str, object]:
    lang = _code(lang)
    strings = _strings(lang)
    return {
        "lang": lang,
        "t": strings,
        "message": message,
        "error": error,
        "example": example or "",
        "next_example": next_example,
        "other_lang": "en" if lang == "hi" else "hi",
        "page_kind": "index",
        "page_title": strings["app_title"],
    }
