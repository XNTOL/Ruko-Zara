# Ruko Zara — Deck narrative

Use this as slide titles, on-slide copy, and spoken lines. Keep slides sparse; the story lives in your voice.

**Live demo:** https://ruko-zara.onrender.com  
**Warm before presenting:** `python scripts/warmup.py https://ruko-zara.onrender.com`  
**Tagline:** Resilience, not returns.

---

## Slide 1 — Title

**On slide**
- रुको ज़रा / Ruko Zara  
- Resilience, not returns  
- SEBI / NSDL Sangyan · Track A  
- Live: ruko-zara.onrender.com  

**Say**  
“This is Ruko Zara — wait a moment. It’s a pause button for forwarded investment tips, before money moves.”

---

## Slide 2 — Problem

**On slide**
- Demat accounts crossed ~16 crore; growth is outside metros  
- Tips arrive on WhatsApp / Telegram as “sure profit”  
- Fake authority + urgency + private groups  
- People learn after withdrawals stop  

**Say**  
“India’s new investors often don’t start with a prospectus. They start with a forward. Scam groups wrap pressure and authority into one message. By the time someone knows it’s wrong, the money is already gone. The gap isn’t more returns advice — it’s a moment of resilience before they act.”

---

## Slide 3 — User

**On slide**
- Sunita-ji — retired teacher, small town  
- Hindi first; English with effort  
- Low-cost Android, unstable network  
- Trusts the relative who forwarded the tip  
- Needs: large text, voice, one calm next step  

**Say**  
“Meet Sunita-ji. She reads Hindi easily. She uses WhatsApp every day. A relative forwards a sure-profit tip into a private group. She trusts the person — she can’t judge the tip. If the product works for her, it works for Bharat-first judging.”

---

## Slide 4 — Journey

**On slide**
1. Open → Hindi by default  
2. Paste tip → जाँचें  
3. See level + reasons + matched words  
4. सुनें (optional)  
5. Pause + official reporting  
6. Copy warning → family group  

**Say**  
“One journey, under ninety seconds. Paste, understand, pause, share. No account. No history. No ‘this is safe.’”

---

## Slide 5 — Solution

**On slide**
- Paste → check → understand → pause  
- Warning signs in plain Hindi / English  
- Proof: the exact matched words  
- Protection: 1930 · cybercrime.gov.in · SEBI SCORES · bank/UPI reminder  
- Family warning card (rule titles only)  

**Say**  
“Ruko Zara doesn’t rate stocks. It names patterns in the message — guaranteed returns, OTP asks, urgency, fake SEBI claims, private channels — and shows the words that triggered them. Then it stops the impulse: don’t send money, don’t share OTP, talk to someone you trust, and use official reporting if needed.”

**Hackathon principles (if asked / backup line)**  
Detect fraud early · recognise misleading info · explain simply · reduce impulse · clarify protection.

---

## Slide 6 — How the score works

**On slide**
- Rules first (deterministic)  
- Levels: **many** / **some** / **few** — never “safe”  
- Strong signs (e.g. sure profit, money/OTP) weigh more  
- Educational “don’t share OTP” wording is not treated as a scam  
- Optional AI line: one summary only; labelled; can be off  

**Say**  
“Scoring is boring on purpose. Patterns in code decide the level. AI never decides risk. If AI is off — as on our free deploy — the full journey still works. That honesty is the product.”

---

## Slide 7 — Guardrails

**On slide**
- No buy / sell / hold / price / target  
- No ads, sign-up, or affiliate links  
- Message never stored; no cookies; no third-party trackers  
- Caveat on every result  
- Links only to official bodies  
- Footer: independent prototype — not SEBI/NSDL  

**Say**  
“These aren’t slogans. They’re disqualifiers if we break them. Judges can paste a tip and verify: nothing is saved, nothing says safe, and every link is an official door — not our door.”

---

## Slide 8 — Technology

**On slide**
- FastAPI + Jinja — server-rendered, works with JS mostly off  
- Tiny CSS/JS — fits slow phones and free hosting  
- Rules in `rules.py`; strings in `content.py`  
- Live on Render (free): ruko-zara.onrender.com  
- Path later: more patterns, on-device, more languages  

**Say**  
“Feasible today: one Docker service, no database, no accounts. Scalable tomorrow: add patterns, not infrastructure. Same engine can move closer to the phone over time.”

---

## Slide 9 — Honest limits & next steps

**On slide**
**Limits**
- New spellings and tricks can slip past word rules  
- We don’t know who sent the message  
- We can’t verify a SEBI number — SEBI’s site can  
- Free host may sleep; warm before demo  

**Next**
- Screenshot / OCR (careful with privacy)  
- Native Hindi sign-off on every string  
- More languages after native review  
- On-device / offline path  

**Say**  
“We’d rather name the limits than overclaim. Ruko Zara buys time — the pause — and points people to real protection. That is resilience, not returns.”

---

## Slide 10 — Close / call to action

**On slide**
- Try it: https://ruko-zara.onrender.com  
- Demo video follows this same journey  
- Question for judges: *Would Sunita-ji pause before she pays?*  

**Say**  
“Open the link. Paste a tip. Watch the pause. That’s the whole pitch.”

---

## Suggested slide count

| # | Title | Time if presenting live |
|---|--------|-------------------------|
| 1 | Title | 20 s |
| 2 | Problem | 45 s |
| 3 | User | 30 s |
| 4 | Journey | 40 s |
| 5 | Solution | 45 s |
| 6 | Score | 40 s |
| 7 | Guardrails | 40 s |
| 8 | Technology | 30 s |
| 9 | Limits & next | 40 s |
| 10 | Close | 20 s |

Total spoken ≈ **5–6 minutes**. Cut slides 6 or 8 if you need a shorter deck; never cut Problem, User, Journey, Guardrails.

---

## One-sentence spine (memorise this)

**Forwarded tips push people to act; Ruko Zara names the warning signs, proves them with matched words, and makes them pause — then points to 1930, cybercrime, and SEBI — without ever calling a tip “safe.”**
