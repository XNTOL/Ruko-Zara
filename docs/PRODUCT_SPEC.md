# Ruko Zara — Product Spec

रुको ज़रा means "wait a moment". Status: MVP spec. Owner: XN (solo). Build window: 1–4 Oct 2026, about 6 hours a day.

## 1. Essence

**Resilience, not returns.** A person pastes a forwarded investment "tip". Ruko Zara shows the warning signs in plain Hindi or English, reads them aloud, and leads the person to a pause before money moves.

The hackathon says the strongest products connect several of its design principles. This one connects five:

| Hackathon principle (PDF §3) | Where Ruko Zara does it |
|---|---|
| Detect a fraud before becoming a victim | Five red-flag rules on the pasted message |
| Recognise misleading information | Reasons shown with the exact matched words |
| Explain in simple language | Plain Hindi/English, read aloud |
| Reduce impulsive decisions | The pause step |
| Clarify protection mechanisms | Reporting list: 1930, cybercrime portal, SEBI SCORES, bank |

Track: **A** (Tip-Group Risk Profiler). Borrowed from Track E: honest uncertainty, no true/false verdict.

## 2. Problem → User → Solution → Technology → Usefulness

The PDF (§8) asks for this chain through one complete user journey.

- **Problem.** Demat accounts passed 16 crore, and most new accounts come from non-metro cities. Many new investors act on social-media "tips". Scam groups on WhatsApp and Telegram use fake authority, pressure, and promises of sure profit. Victims learn the truth when withdrawals stop.
- **User.** See §3.
- **Solution.** Paste, check, understand, pause. One screen in, one screen out.
- **Technology.** Deterministic rules decide the level. An AI model writes one short summary. Browser speech reads the result aloud. A small server-rendered Python app runs on a low-end phone.
- **Real-world usefulness.** A family member can use it in 30 seconds. A person can send the warning back to the family group. The rules grow by adding patterns. The same engine can later run on the device, offline.

## 3. Target user

**Persona (fictional): Sunita-ji.** A retired schoolteacher in a small town. She reads Hindi with ease and English with effort. She uses WhatsApp daily on a low-cost Android phone with an unstable connection. A relative forwards her a "sure-profit" tip with a link to a private group. She trusts the relative. She cannot judge the tip.

She needs: large text, Hindi first, voice, one clear action per screen, and a calm tone that does not scare her.

Secondary user: the relative or younger family member who wants a quick second opinion.

## 4. The journey (J1)

1. Sunita-ji opens the link on her phone. Hindi shows by default.
2. She pastes the forwarded message and taps **जाँचें**.
3. The result shows one level, the reasons, and the matched words.
4. She taps **सुनें**. The phone reads the result in Hindi.
5. She sees the **pause step** and the reporting list.
6. She taps **चेतावनी कॉपी करें** and sends the warning card to the family group.

**Completion criterion for J1:** a tester completes steps 1–6 on a real Android phone, on a slow connection, with the AI switched off, in under 90 seconds and without help.

## 5. Scope

**MVP (must).** FR-1 to FR-8, FR-10 to FR-12.

**Stretch (Day 3, if time remains).** FR-9 warning card. XN chose this over screenshot input and a third language.

**Out of scope.** Each item below has a reason. Name them in the deck as "next steps".

- Screenshot or image input (sends more private data to an AI; needs OCR).
- Live registry lookup (no open API found; the app links to SEBI's own search).
- Accounts, history, push alerts, analytics.
- Any language beyond Hindi and English (needs a native-speaker check).
- Any market data, stock page, or price.

## 6. Guardrails as testable requirements

These come from PDF §4 and §7. A break disqualifies the entry.

| ID | Requirement | How to test |
|---|---|---|
| G1 | No stock tip, buy/sell/hold, price, target, or prediction in any output. | Output-validator test (see ARCHITECTURE §6). Corpus test on all fixed strings. |
| G2 | No monetisation. No ad, affiliate link, sign-up, paywall, or upsell. Links go only to official bodies. | Link-allowlist test over all templates and `content.py`. |
| G3 | Privacy by design. No storage of the message. No cookie. No third-party script, font, or analytics. Masking runs before any AI call. Logs hold no message text. The app asks for no SMS, contacts, or notification permission. | Test: logs captured during a request contain no part of the message. Test: response headers set no cookie. |
| G4 | Honest uncertainty. No output says "safe". The caveat shows at every level. The AI line is labelled. | Test: every result page contains the caveat. Validator rejects "safe"/"सुरक्षित" in AI text. |
| G5 | Public-good ethos. The footer states: independent prototype, not an official SEBI or NSDL service. | Template test. |
| G6 | Facts from a human. Phone numbers and URLs live in `content.py` only, each checked by a person. | Review checklist, §10. |

## 7. Functional requirements

| ID | Requirement |
|---|---|
| FR-1 | Input: one text area. Maximum 2000 characters. An empty message or one under 5 characters shows an inline error. |
| FR-2 | Assess: call `assess(text)` in `app/rules.py`. The result is one of `many`, `some`, `few`. |
| FR-3 | Result: show the level, each reason (title, why, matched words), and the caveat. |
| FR-4 | Language: Hindi default, English on request. The whole page switches. The choice travels in the URL (`?lang=hi`), never in a cookie. |
| FR-5 | Read aloud: a **सुनें / Listen** button reads the level, the reasons, and the pause step. If the phone has no voice for the language, the button explains this in text. |
| FR-6 | SEBI number: when the message holds a number such as `INA…`, show it, say "this tool cannot verify it", and link to SEBI's own search. When the message claims SEBI registration with no number, say so. |
| FR-7 | AI summary: one or two sentences, optional. Shown only if it passes the validator. Labelled as AI-written. |
| FR-8 | Pause step and reporting list, shown at every level. Content: UIUX §6. |
| FR-9 | Warning card (stretch): a short text the user copies and sends to a group. It holds rule titles only, never the original message. |
| FR-10 | Examples: three synthetic messages (scam, educational warning, borderline) load into the text area with one tap. They serve the demo and the judges. |
| FR-11 | `/about` page: how it works, what is stored (nothing), the honest limits (§9). |
| FR-12 | The core journey works with JavaScript off, except read-aloud and copy. |

## 8. Scoring behavior

`app/rules.py` is the single source for patterns and for the level logic. This table describes the behavior only.

| Rule | Strength | Example sign |
|---|---|---|
| `guaranteed_returns` | strong | "100% sure profit", "पक्का मुनाफा" |
| `money_or_access` | strong | registration fee, "share your OTP", screen-share apps |
| `urgency` | medium | "only today", "आज ही" |
| `fake_authority` | medium | "SEBI approved", "insider", "operator" |
| `private_channel` | medium | "join VIP Telegram", `t.me/…`, "download app" |

- **many:** one strong sign, or three or more signs.
- **some:** exactly two signs.
- **few:** zero or one medium sign.
- A match is skipped when nearby words show the message **warns against** it ("never share your OTP").

## 9. Honest limits (state them in the deck and on `/about`)

- Rules read words. New tricks and spelling changes can slip past. Tests show where.
- The tool does not know who sent the message.
- The tool cannot verify a SEBI number. SEBI's own search can.
- Hindi voice depends on the phone.
- The AI summary can contain mistakes.
- A free host may need a few seconds to wake up.

## 10. Definition of done

Every line is checkable.

- [ ] J1 passes (§4).
- [ ] G1–G6 tests pass.
- [ ] Test corpus has at least 20 synthetic messages in Hindi, English, and Hinglish: scam, educational, borderline. XN writes the first set.
- [ ] A native Hindi reader approved every Hindi string. No `# REVIEW` tag remains.
- [ ] 1930, `cybercrime.gov.in`, and the SEBI SCORES address were opened and checked by a person on the day of submission.
- [ ] Page weight and accessibility budgets pass (ARCHITECTURE §8, UIUX §8).
- [ ] The live link works on a phone on mobile data.

## 11. Evaluation map (PDF §9)

| Criterion | Weight | Proof in the demo |
|---|---|---|
| Resilience & safety impact | 30% | Real scam patterns flagged; pause step; reporting list; warning card to the family group |
| Tier-2/3 usability (Bharat-first) | 25% | Hindi default; voice; large text; works on slow network and with JS off; under 100 KB |
| Guardrail compliance & trust | 15% | Nothing stored; no "safe" verdict; labelled AI line; official links only; stated limits |
| Technical execution | 15% | Rules first, AI second; output validator; fallback; masking before AI |
| Feasibility & scalability | 15% | Stateless app; rules extend by pattern; path to on-device and more languages |

## 12. Submission pack (PDF §8)

**Live demo link.** Hosted app. Warm it before judging.

**Video, 3–5 minutes.** Beats:
1. Sunita-ji gets the forwarded tip (20 s).
2. She pastes and checks (30 s).
3. Result in Hindi, with matched words (40 s).
4. She taps Listen (30 s).
5. Pause step and reporting list (40 s).
6. Warning card to the family group (30 s).
7. A harmless educational message gets "few signs", with the caveat (30 s).
8. How it works and the honest limits (40 s).

**Deck outline.** 1 Problem. 2 User. 3 Journey. 4 Solution. 5 How the score works. 6 Guardrails. 7 Technology. 8 Honest limits and next steps.

## 13. Open items for XN

1. Write the first sample messages.
2. Review the Hindi strings.
3. Create a free Groq account and key (Day 3).
4. Choose the host (Day 4).
5. Check the exact submission time on the Discord.
