# Ruko Zara (रुको ज़रा)

Investor-protection web app for the SEBI / NSDL Sangyan hackathon (1–4 Oct 2026). Resilience, not returns.
A person pastes a forwarded "tip". The app lists warning signs in Hindi or English, reads them aloud, and leads the person to a pause before money moves.

## Pointers

- Read `docs/PRODUCT_SPEC.md` before you change behavior, scoring, wording of a result, or any guardrail.
- Read `docs/ARCHITECTURE.md` before you add a file, dependency, route, environment variable, or network call.
- Read `docs/UIUX_SPEC.md` before you touch a template, style, script, or user-facing string.
- Work through the tasks in `docs/ARCHITECTURE.md` §11 in order. One task per change. A task is done when its completion criterion passes.

## Guardrails (disqualifying if broken)

Each line gives the target first.

- Output describes **patterns in the message**. An instrument named in the input never appears in the output as advice, rating, or prediction.
- Output points only to official bodies (1930, cybercrime.gov.in, SEBI). No ads, affiliate links, sign-up, or upsell.
- The message exists in memory for one request. No database, no file write, no cookie, no third-party script or font. Logs hold level and rule ids only.
- Every result carries the caveat from `app/content.py`. The lowest level reads "few warning signs found", never "safe".
- AI writes one short summary only. Rules decide the level. The app works with AI off.

## Conventions the code cannot show

- All user-facing text lives in `app/content.py`, in Hindi and English. Mark every new Hindi string `# REVIEW`. A native reader approves it.
- Patterns live in `app/rules.py` only. Add a test case in `tests/` for every pattern you add or change.
- Run `python -m pytest` before you call a task done. Keep it _tight_: no network in tests.
- Test messages are synthetic. Use no real name, brand, or phone number.
