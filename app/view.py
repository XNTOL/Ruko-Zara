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
        "report": [
            {"key": "1930", "text": strings["report_1930"], "href": LINKS["helpline"]},
            {
                "key": "portal",
                "text": strings["report_portal"],
                "href": LINKS["cybercrime"],
            },
            {"key": "scores", "text": strings["report_scores"], "href": LINKS["scores"]},
            {"key": "bank", "text": strings["report_bank"], "href": None},
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


def build_view(
    result: Result,
    summary: str | None,
    lang: str,
) -> dict[str, object]:
    """Return the dict passed to result.html (ARCHITECTURE §3)."""
    lang = _code(lang)
    strings = _strings(lang)
    reasons = _reasons(result, lang)
    level_title = LEVELS[result.level][lang]

    return {
        "lang": lang,
        "level": result.level,
        "level_title": level_title,
        "reasons": reasons,
        "caveat": CAVEAT[lang],
        "summary": summary,
        "sebi": _sebi(result, lang),
        "pause": _pause(lang),
        "card_text": _card_text(result, lang),
        "speak_text": _speak_text(level_title, reasons, lang),
        "t": strings,
        "other_lang": "en" if lang == "hi" else "hi",
        "page_kind": "result",
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
