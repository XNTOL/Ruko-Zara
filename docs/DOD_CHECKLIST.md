# Definition of Done — PRODUCT_SPEC §10

Status key: **DONE** = automated or verified in repo · **HUMAN** = needs a person on submission day · **PENDING** = not finished in repo

| Item | Status | Notes |
| ---- | ------ | ----- |
| J1 passes (PRODUCT_SPEC §4) | HUMAN | Real Android phone, slow network, AI off, under 90 s |
| G1–G6 tests pass | DONE | `test_content`, `test_routes`, `test_explain`, `test_privacy`, `test_budget_a11y` (93 pass, 1 xfail) |
| Test corpus ≥ 20 synthetic messages (hi / en / Hinglish; scam, edu, borderline) | DONE | `tests/test_rules.py` CORPUS |
| Native Hindi reader approved every Hindi string; no `# REVIEW` | PENDING | `# REVIEW` still on Hindi in `app/content.py`; `test_no_review_tags_remain` is xfail until cleared |
| 1930, cybercrime.gov.in, SEBI SCORES opened and checked on submission day | HUMAN | Wired in repo: `tel:1930`, `https://www.cybercrime.gov.in/`, `https://scores.sebi.gov.in/` only via `app/content.py` (G6); bank/UPI is a non-link note |
| Page weight and accessibility budgets pass | DONE | `tests/test_budget_a11y.py` + UIUX §8 CSS rules |
| Live link works on a phone on mobile data | HUMAN | Live: https://ruko-zara.onrender.com (`/healthz` ok); confirm on phone + mobile data; warm with `scripts/warmup.py` |

## Automated UIUX §8 checks in CI

- First load (`/` + `app.css` + `app.js`) ≤ 100 KB
- `app.css` ≤ 12 KB, `app.js` ≤ 8 KB
- Body 20 px, `--tap: 56px`, focus outline, `prefers-reduced-motion`, `overflow-x`
- No green / checkmark styling
- Hindi default; result works without JS for the POST path
- Pause + report + caveat on all levels (`test_routes.py`)
- Report list: `tel:1930` (call), cybercrime + SCORES as web links, bank/UPI as note (not `<a>`)

## Remaining for submission day

1. Deploy and confirm the live URL on mobile data.
2. Open and click-check 1930 (dialer on phone), cybercrime.gov.in, and SEBI SCORES.
3. Run J1 on a real phone.
4. Native Hindi pass: remove every `# REVIEW` once approved.
