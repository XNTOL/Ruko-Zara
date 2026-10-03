# Ruko Zara (रुको ज़रा)

**[Open the app →](https://ruko-zara.onrender.com)**

Paste a forwarded investment tip. Get clear warning signs in Hindi or English, a pause step, and official reporting links — before money moves. Never says a tip is “safe.” Never gives buy/sell advice.

Free host may sleep after idle time. First open can take ~30–60s. Before a demo:

```bash
python scripts/warmup.py https://ruko-zara.onrender.com
```

## What it does

1. Paste the message.
2. See `many` / `some` / `few` warning signs with matched words.
3. Pause. Call **1930**, open **cybercrime.gov.in** or **SEBI SCORES**, or tell your bank/UPI (reminder only).
4. Optional: listen aloud, copy a short warning for family (rule titles only — the original message is never stored).

## Guardrails

- No stock tips, prices, targets, or “safe” verdicts
- No ads, accounts, or cookies
- One request in memory only; logs never keep the pasted text
- Links only to official bodies (1930, cybercrime portal, SEBI)
- Independent prototype — **not** an official SEBI or NSDL service

## Local run (optional)

```bash
python -m pip install -r requirements-dev.txt
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Tests: `python -m pytest`  
Health: `GET /healthz` → `{"ok": true}`

AI summary (Groq) shows under the reasons when enabled. Put the key only in Render/local env — never in git. Copy `.env.example` → `.env`, set `AI_API_KEY`, and `AI_ENABLED=true`. On Render: Environment → secret `AI_API_KEY` + `AI_ENABLED=true`.

## Specs

- [PRODUCT_SPEC](docs/PRODUCT_SPEC.md) · [ARCHITECTURE](docs/ARCHITECTURE.md) · [UIUX](docs/UIUX_SPEC.md) · [AGENTS](docs/AGENTS.md) · [DoD](docs/DOD_CHECKLIST.md)
