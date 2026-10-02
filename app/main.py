"""FastAPI entrypoint: health check + tracer-bullet check flow (T2)."""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.content import CAVEAT, LEVELS, STRINGS, TEXT, t as t_str
from app.rules import Result, assess

BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(title="Ruko Zara")

MAX_CHARS = int(os.getenv("MAX_CHARS", "2000"))
MIN_CHARS = 5

# Synthetic examples only (AGENTS.md). No real names, brands, or phones.
EXAMPLES: dict[str, str] = {
    "scam": (
        "100% sure profit this week. Share your OTP and pay the registration fee. "
        "Join VIP Telegram t.me/tipsdemo and act now, only today."
    ),
    "edu": (
        "Never share your OTP with anyone. Do not join private Telegram tip groups. "
        "Ignore messages that promise guaranteed returns. This is a scam warning."
    ),
    "border": "Seats are limited. Reply only today if you want more details.",
}


def _lang(value: str | None) -> str:
    return "en" if (value or "").lower() == "en" else "hi"


def _strings(lang: str) -> dict[str, str]:
    return STRINGS["en" if lang == "en" else "hi"]


def _reasons(result: Result, lang: str) -> list[dict[str, object]]:
    code = "en" if lang == "en" else "hi"
    out: list[dict[str, object]] = []
    for finding in result.findings:
        copy = TEXT[finding.rule]
        out.append(
            {
                "rule": finding.rule,
                "title": copy["title"][code],
                "why": copy["why"][code],
                "evidence": list(finding.evidence),
            }
        )
    return out


@app.get("/healthz")
def healthz() -> dict[str, bool]:
    return {"ok": True}


@app.get("/", response_class=HTMLResponse)
def index(
    request: Request,
    lang: str = "hi",
    example: str | None = None,
) -> HTMLResponse:
    lang = _lang(lang)
    message = EXAMPLES.get(example or "", "")
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "lang": lang,
            "t": _strings(lang),
            "message": message,
            "error": None,
        },
    )


@app.post("/check", response_class=HTMLResponse)
async def check(
    request: Request,
    message: str = Form(""),
    lang: str = Form("hi"),
) -> HTMLResponse:
    lang = _lang(lang)
    strings = _strings(lang)
    trimmed = (message or "").strip()

    error_key: str | None = None
    if len(trimmed) < MIN_CHARS:
        error_key = "error_empty"
    elif len(trimmed) > MAX_CHARS:
        error_key = "error_long"

    if error_key:
        return templates.TemplateResponse(
            request,
            "index.html",
            {
                "lang": lang,
                "t": strings,
                "message": message,
                "error": strings[error_key],
            },
            status_code=422,
        )

    result = assess(trimmed)
    code = "en" if lang == "en" else "hi"
    level_title = LEVELS[result.level][code]
    reasons = _reasons(result, lang)

    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "lang": lang,
            "t": strings,
            "level": result.level,
            "level_title": level_title,
            "reasons": reasons,
            "caveat": CAVEAT[code],
            "section_none": t_str(lang, "section_none"),
        },
        status_code=200,
    )
