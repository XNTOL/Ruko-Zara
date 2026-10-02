# Ruko Zara (रुको ज़रा)

**Resilience, not returns.** Investor-protection web app for the SEBI / NSDL Sangyan hackathon.

Paste a forwarded investment “tip”. The app lists warning signs in **Hindi** or **English** (including Hinglish), can read them aloud, and leads the person to pause before money moves. It never says a tip is “safe”, and it never gives buy/sell advice.

## Features

- Deterministic red-flag rules (`many` / `some` / `few`) with matched words shown as proof
- Hindi default; in-place language switch on the result page
- Optional AI one-line summary (rules decide the level; app works with AI off)
- Listen (browser speech) with fallback if no voice is available
- Pause steps + reporting links (1930, cybercrime.gov.in, SEBI SCORES)
- Copyable family-group warning card (rule titles only — original message is never stored or echoed)



## Stack

- **Backend / UI:** FastAPI + Jinja2 (server-rendered HTML)
- **Static:** plain CSS/JS (no build step, no JS framework)
- **Optional AI:** OpenAI-compatible HTTP API via `httpx` (e.g. Groq)
- **Deploy:** single Docker web service (Render-ready)



## Quick start (local)

```bash
python -m pip install -r requirements-dev.txt
cp .env.example .env   # optional; set AI_* if you want summaries
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

Health check: `GET /healthz` → `{"ok": true}`.

## Tests

```bash
python -m pip install -r requirements-dev.txt
python -m pytest
```

Tests are offline and should finish in a few seconds. Production Docker installs only `requirements.txt` (no pytest).

## Environment variables


| Variable             | Default                          | Notes                                              |
| -------------------- | -------------------------------- | -------------------------------------------------- |
| `AI_ENABLED`         | `false`                          | Set `true` only when `AI_API_KEY` and `AI_MODEL` are set |
| `AI_API_KEY`         | *(empty)*                        | Required for summaries                             |
| `AI_BASE_URL`        | `https://api.groq.com/openai/v1` | OpenAI-compatible base URL                         |
| `AI_MODEL`           | *(empty)*                        | Required for summaries (pick a current free model) |
| `AI_TIMEOUT_S`       | `4`                              | AI HTTP timeout                                    |
| `MAX_CHARS`          | `2000`                           | Max pasted message length                          |
| `RATE_LIMIT_PER_MIN` | `12`                             | Per-IP AI rate limit (in memory)                   |
| `DAILY_AI_CAP`       | `500`                            | Process-local daily AI cap                         |


If the key or model is missing, the check page still works; the AI block is simply omitted.

## Project layout

```
app/
  main.py          Routes, security headers
  rules.py         Patterns + assess()
  privacy.py       mask_sensitive() before AI
  explain.py       Optional AI summary + validator
  content.py       All user-facing hi/en strings
  view.py          Template view-model
  templates/       Jinja HTML
  static/          app.css, app.js
docs/              Product, architecture, UI/UX specs
tests/             pytest suite
Dockerfile         Production image (binds 0.0.0.0:$PORT)
render.yaml        Optional Render Blueprint
scripts/warmup.py  Ping /healthz before a demo (free hosts may sleep)
```



## Deploy (Render)

1. Push this repo to GitHub/GitLab and connect it to Render.
2. Create a **Web Service** with **Docker** runtime (or use `render.yaml`).
3. Health check path: `/healthz`.
4. Leave `AI_ENABLED=false` until you set `AI_API_KEY` and `AI_MODEL` in the Dashboard, then flip `AI_ENABLED=true`.
5. Before a live demo on a free tier:  
   `python scripts/warmup.py https://your-service.onrender.com`

Start command (from the Dockerfile):

```bash
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
```



## Guardrails

- No stock tips, prices, targets, or “safe” verdicts.
- No ads, affiliate links, accounts, or cookies.
- Message lives in memory for one request only; logs never store the pasted text.
- Links only to official bodies (1930, cybercrime portal, SEBI).
- Independent prototype — **not** an official SEBI or NSDL service.



## Specs for contributors

Read these before changing behavior or UI:

- [docs/PRODUCT_SPEC.md](docs/PRODUCT_SPEC.md)
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- [docs/UIUX_SPEC.md](docs/UIUX_SPEC.md)
- [docs/AGENTS.md](docs/AGENTS.md)
- [docs/DOD_CHECKLIST.md](docs/DOD_CHECKLIST.md) — definition of done

New Hindi strings in `app/content.py` should be marked `# REVIEW` until a native reader approves them. Add a test for every new or changed pattern in `app/rules.py`.