"""FastAPI entrypoint: routes, templates, security headers."""

from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.content import STRINGS
from app.rules import assess
from app.view import build_about, build_index, build_view

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

_EXAMPLE_ORDER = ("scam", "edu", "border")

_SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; script-src 'self'; style-src 'self'; "
        "img-src 'self' data:; base-uri 'none'; form-action 'self'"
    ),
    "Referrer-Policy": "no-referrer",
    "X-Content-Type-Options": "nosniff",
}


def _lang(value: str | None) -> str:
    return "en" if (value or "").lower() == "en" else "hi"


def _next_example(current: str | None) -> str:
    if current in _EXAMPLE_ORDER:
        idx = (_EXAMPLE_ORDER.index(current) + 1) % len(_EXAMPLE_ORDER)
        return _EXAMPLE_ORDER[idx]
    return "scam"


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    for key, value in _SECURITY_HEADERS.items():
        response.headers[key] = value
    if request.url.path == "/check":
        response.headers["Cache-Control"] = "no-store"
    return response


@app.exception_handler(Exception)
async def unhandled_error(request: Request, exc: Exception) -> HTMLResponse:
    if isinstance(exc, (HTTPException, StarletteHTTPException, RequestValidationError)):
        raise exc
    lang = _lang(request.query_params.get("lang"))
    strings = STRINGS[lang]
    return templates.TemplateResponse(
        request,
        "error.html",
        {
            "lang": lang,
            "t": strings,
            "other_lang": "en" if lang == "hi" else "hi",
            "page_kind": "error",
            "page_title": strings["error_server"],
            "example": "",
        },
        status_code=500,
    )


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
    key = example if example in EXAMPLES else None
    vm = build_index(
        lang,
        message=EXAMPLES.get(key or "", ""),
        error=None,
        example=key,
        next_example=_next_example(key),
    )
    return templates.TemplateResponse(request, "index.html", vm)


@app.get("/about", response_class=HTMLResponse)
def about(request: Request, lang: str = "hi") -> HTMLResponse:
    vm = build_about(_lang(lang))
    vm["example"] = ""
    return templates.TemplateResponse(request, "about.html", vm)


@app.post("/check", response_class=HTMLResponse)
async def check(
    request: Request,
    message: str = Form(""),
    lang: str = Form("hi"),
) -> HTMLResponse:
    lang = _lang(lang)
    trimmed = (message or "").strip()

    error_key: str | None = None
    if len(trimmed) < MIN_CHARS:
        error_key = "error_empty"
    elif len(trimmed) > MAX_CHARS:
        error_key = "error_long"

    if error_key:
        strings = STRINGS[lang]
        vm = build_index(
            lang,
            message=message,
            error=strings[error_key],
            example=None,
            next_example="scam",
        )
        return templates.TemplateResponse(
            request,
            "index.html",
            vm,
            status_code=422,
        )

    result = assess(trimmed)
    # AI summary comes in T7; tracer keeps summary None so the app works AI-off.
    vm = build_view(result, summary=None, lang=lang)
    vm["example"] = ""
    return templates.TemplateResponse(request, "result.html", vm, status_code=200)
