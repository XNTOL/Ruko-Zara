# Ruko Zara — UI/UX Spec

Read `PRODUCT_SPEC.md` §3–§4 first. Design for Sunita-ji: a Hindi reader on a low-cost Android phone, on a slow connection, who trusts the sender of the tip.

## 1. Principles

1. **One screen, one action.** The form has one main button. The result has one main button (Listen).
2. **Hindi first.** Hindi shows by default. English is one tap away.
3. **Calm, not scary.** The tone is a helpful neighbour. No red alarm screens, no all-capital shouting.
4. **Words, icon, and colour together.** A level always has text and an icon. Colour never works alone.
5. **No green.** No result uses green or a check mark. Green reads as "safe", and the tool never says "safe". The lowest level uses calm blue.
6. **Show the proof.** Each reason shows the exact matched words from the message, highlighted. The user sees why.
7. **Light.** No images, no web fonts, no animation beyond a 150 ms fade.

## 2. Design tokens

| Token | Value | Use |
|---|---|---|
| `--bg` | `#FAF7F2` | Page background |
| `--text` | `#1F2933` | Body text. 13.8:1 on `--bg` |
| `--muted` | `#4B5563` | Hints. 7.1:1 |
| `--primary` | `#1F4E79` | Buttons, links. White text on it: 8.7:1 |
| `--many-bg` / `--many-bd` / `--many-tx` | `#FDECEA` / `#B42318` / `#7A1710` | Level "many". Text 9.4:1 |
| `--some-bg` / `--some-bd` / `--some-tx` | `#FFF4E0` / `#B54708` / `#7A2E0E` | Level "some". Text 8.7:1 |
| `--few-bg` / `--few-bd` / `--few-tx` | `#EAF1F8` / `#1F4E79` / `#12304D` | Level "few". Text 11.9:1 |
| Font stack | `"Noto Sans Devanagari","Noto Sans","Mangal",system-ui,sans-serif` | No web font loads |
| Body size | 20 px, line height 1.6 | Hindi needs room |
| Heading size | 26 px, weight 700 | |
| Tap target | 56 px high at least, 8 px gap | Large thumbs, shaky hands |
| Page width | fluid, max 640 px, 16 px side padding | Design at 360 px first |
| Focus ring | 3 px `--primary` outline, 2 px offset | Keyboard and switch users |

Level icons are inline SVG: `many` = triangle with "!", `some` = circle with "!", `few` = circle with "i".

Use dark text on light cards only. Add `prefers-reduced-motion` support.

## 3. Screen S1 — Check (`/`)

```
┌──────────────────────────────┐
│ रुको ज़रा        [हिन्दी|EN] │  header: title left, language right
│                              │
│ पैसे भेजने से पहले,           │  tagline
│ एक बार रुकें और जाँचें।       │
│                              │
│ जो संदेश आया है, उसे          │  label
│ यहाँ चिपकाएँ                  │
│ ┌──────────────────────────┐ │
│ │                          │ │  text area, 8 rows
│ │                          │ │
│ └──────────────────────────┘ │
│ OTP, बैंक खाता नंबर या पासवर्ड │  privacy hint (muted)
│ न डालें। आपका संदेश कहीं सेव  │
│ नहीं होता।                    │
│                              │
│ [        जाँचें        ]     │  primary, full width, 56 px
│ [   उदाहरण देखें   ]         │  secondary, outlined
│                              │
│ इस ऐप के बारे में · footer   │
└──────────────────────────────┘
```

- The language switch is two links (`?lang=hi`, `?lang=en`). The active one is bold with an underline.
- The label is tied to the text area (`for`/`id`). Placeholder text is not a label.
- **See an example** is a link to `/?example=scam` (and `edu`, `border`). It cycles through the three examples. No JS needed.
- The privacy hint sits directly above the button. It does not hide in a footer.

## 4. Screen S2 — Result (`POST /check`)

Block order, top to bottom. Each block is one idea.

```
┌──────────────────────────────┐
│ रुको ज़रा        [हिन्दी|EN] │
│ ┌──────────────────────────┐ │
│ │ ▲  बहुत से चेतावनी संकेत  │ │  1. LEVEL CARD (many bg, icon + text)
│ └──────────────────────────┘ │
│ [   🔊  सुनें   ]            │  2. LISTEN (primary, full width)
│                              │
│ ये संकेत मिले                 │  3. REASONS
│ ┌──────────────────────────┐ │
│ │ पक्के मुनाफ़े का वादा      │ │    title (bold)
│ │ बाज़ार में मुनाफ़े की ...   │ │    why (one or two sentences)
│ │ मिला: [100% sure profit] │ │    matched words, highlighted
│ └──────────────────────────┘ │
│ ... one card per reason ...  │
│                              │
│ ┌ AI-written summary ──────┐ │  4. AI SUMMARY (only if valid)
│ │ ...                      │ │    label above it
│ └──────────────────────────┘ │
│ [SEBI number block]          │  5. only if a number or a claim is found
│                              │
│ ┌ अभी रुकें ───────────────┐ │  6. PAUSE STEP (3 lines, large)
│ │ 1 पैसे न भेजें ...        │ │
│ └──────────────────────────┘ │
│ पैसे चले गए हों ... बताएँ      │  7. REPORT LIST (tap-to-call 1930, links)
│ ┌ परिवार के ग्रुप के लिए ──┐ │  8. WARNING CARD (stretch)
│ │ [ चेतावनी कॉपी करें ]     │ │
│ └──────────────────────────┘ │
│ caveat                       │  9. CAVEAT (muted, always)
│ [दूसरा संदेश जाँचें]          │  10. CHECK ANOTHER
│ footer                       │
└──────────────────────────────┘
```

- Level card: title at 26 px bold, icon 32 px, left border 6 px in `--*-bd`.
- Matched words use `<mark>` with a bold weight and an underline. Colour is not the only cue.
- Level `few` and `no_text`: block 3 shows the `section_none` line instead of the reason cards.
- Block 5 text comes from `sebi_found` / `sebi_claim_no_number`. The button **Check on SEBI website** is a link to SEBI's own search (a human verifies the address; see PRODUCT_SPEC G6).
- Block 7 links: `tel:1930`, the cybercrime portal, SEBI SCORES. Each opens in the same tab with `rel="noopener noreferrer"`.
- The result page keeps the typed message out of the page. It shows only matched words, so the page is safe to screen-share.
- The page title changes to the level title, for screen readers.

## 5. States and behavior

| State | Behavior |
|---|---|
| Empty or very short message | Return to S1. Error text above the text area, in `--many-tx`, with an icon. Focus moves to the text area. |
| Too long | Same, with `error_long`. The text area keeps the typed text. |
| Waiting | The button turns into `loading` text and is disabled. Needs a small JS handler; without JS the browser waits as usual. |
| AI unavailable | Block 4 is absent. Nothing else changes. No error shows. |
| Voice supported | **Listen** reads `speak_text` with the page language (`hi-IN` or `en-IN`). While reading, the button reads **Stop**. |
| Voice not supported for the language | Hide the button. Show `voice_none` in muted text. |
| Copy | Copy `card_text`. On success the button reads `copied` for 2 seconds. If the Clipboard API fails, select the card text and ask the user to copy it. |
| Server error | `error.html` with `error_server` and a link back to S1. |
| Language switch | Plain links. The result page cannot be re-opened by GET, since the message is not stored. The switch on S2 re-submits nothing. It links to S1 in the other language. |

`speak_text` order: level title, then each reason title, then the three pause lines. Nothing else.

## 6. Pause step and reporting content

Shown at **every** level. At `few`, show `section_none` above them.

**Pause (3 lines):** `pause_1`, `pause_2`, `pause_3`.

**Report list (4 lines), in this order:**
1. `report_1930` — `tel:1930` link.
2. `report_portal` — link to the cybercrime portal.
3. `report_scores` — link to SEBI SCORES.
4. `report_bank` — text only.

**Warning card text** (FR-9). Build from the rule titles found. Never quote the original message.

- hi: `⚠️ रुको ज़रा! एक संदेश में ये चेतावनी संकेत मिले: {titles}। पैसे न भेजें, कोई लिंक न खोलें, OTP न बताएं। ठगी हो जाए तो 1930 पर बताएं।`
- en: `⚠️ Ruko Zara! A message showed these warning signs: {titles}. Do not send money, open any link, or share an OTP. If you were cheated, call 1930.`

## 7. Copy deck

This deck is the first content of `app/content.py`. **All Hindi text needs a native reader's approval.** Mark each Hindi string `# REVIEW` until then. Keep gender-neutral phrasing for the tool.

| Key | Hindi (hi) | English (en) |
|---|---|---|
| `app_title` | रुको ज़रा | Ruko Zara |
| `tagline` | पैसे भेजने से पहले, एक बार रुकें और जाँचें। | Before you send money, stop and check. |
| `input_label` | जो संदेश आया है, उसे यहाँ चिपकाएँ | Paste the message you received |
| `privacy_hint` | OTP, बैंक खाता नंबर या पासवर्ड न डालें। आपका संदेश कहीं सेव नहीं होता। | Do not paste an OTP, bank account number, or password. Your message is not saved. |
| `btn_check` | जाँचें | Check |
| `btn_example` | उदाहरण देखें | See an example |
| `btn_listen` | सुनें | Listen |
| `btn_stop` | रोकें | Stop |
| `btn_again` | दूसरा संदेश जाँचें | Check another message |
| `btn_copy` | चेतावनी कॉपी करें | Copy warning |
| `copied` | कॉपी हो गया | Copied |
| `loading` | जाँच जारी है… | Checking… |
| `section_reasons` | ये संकेत मिले | Signs found |
| `section_none` | कोई साफ़ संकेत नहीं मिला। फिर भी पैसे भेजने से पहले परिवार में किसी से पूछें। | No clear signs found. Still, ask someone in your family before you send money. |
| `matched` | संदेश में मिला: | Found in the message: |
| `ai_label` | एआई द्वारा लिखा सारांश। इसमें गलती हो सकती है। | AI-written summary. It can contain mistakes. |
| `pause_title` | अभी रुकें | Pause now |
| `pause_1` | पैसे न भेजें और कोई लिंक न खोलें। | Do not send money. Do not open any link. |
| `pause_2` | OTP, पिन या पासवर्ड किसी को न बताएं। | Do not tell anyone an OTP, PIN, or password. |
| `pause_3` | परिवार के किसी भरोसेमंद व्यक्ति से बात करें। | Talk to a family member you trust. |
| `report_title` | पैसे चले गए हों या शक हो, तो यहाँ बताएँ | If money is gone, or you have a doubt, report here |
| `report_1930` | साइबर ठगी हेल्पलाइन: 1930 (हर समय चालू) | Cyber fraud helpline: 1930 (open at all hours) |
| `report_portal` | cybercrime.gov.in पर शिकायत करें | File a complaint at cybercrime.gov.in |
| `report_scores` | ब्रोकर या म्यूचुअल फंड की शिकायत: सेबी SCORES | Complaint about a broker or mutual fund: SEBI SCORES |
| `report_bank` | अपने बैंक या UPI ऐप को तुरंत बताएँ | Tell your bank or UPI app at once |
| `sebi_found` | संदेश में यह नंबर मिला: {number}। यह टूल इसकी जाँच नहीं कर सकता। सेबी की वेबसाइट पर खुद जाँचें। | This number was found in the message: {number}. This tool cannot verify it. Check it yourself on the SEBI website. |
| `sebi_claim_no_number` | संदेश में सेबी रजिस्ट्रेशन का दावा है, पर कोई नंबर नहीं दिया गया। | The message claims SEBI registration but gives no number. |
| `btn_sebi` | सेबी की वेबसाइट पर जाँचें | Check on the SEBI website |
| `card_title` | परिवार के ग्रुप के लिए चेतावनी | Warning for your family group |
| `voice_none` | इस फ़ोन पर आवाज़ उपलब्ध नहीं है। | Voice is not available on this phone. |
| `error_empty` | पहले संदेश चिपकाएँ। | Paste a message first. |
| `error_long` | संदेश बहुत लंबा है। मुख्य हिस्सा चिपकाएँ। | The message is too long. Paste the main part. |
| `error_server` | कुछ गड़बड़ हो गई। कृपया दोबारा कोशिश करें। | Something went wrong. Please try again. |
| `footer` | यह एक स्वतंत्र प्रोटोटाइप है, सेबी या एनएसडीएल की आधिकारिक सेवा नहीं। | This is an independent prototype. It is not an official SEBI or NSDL service. |
| `about_link` | इस ऐप के बारे में | About this app |

Level titles and the caveat already exist in `rules.py` (`LEVELS`, `CAVEAT`) and move to `content.py` in task T1. The five rule titles and reasons (`TEXT`) move with them.

## 8. Acceptance checks

Each check is yes or no.

**Layout and reading**
- [ ] At 360 px width, nothing scrolls sideways.
- [ ] Body text is 20 px or larger. Hindi lines are not clipped.
- [ ] Every button and link is 56 px high or more, with an 8 px gap.
- [ ] Tab order follows the visual order. Focus ring is always visible.

**Colour and meaning**
- [ ] Every level shows an icon and text, not colour alone.
- [ ] No green and no check mark appears on any result.
- [ ] All text pairs reach WCAG AA (the tokens in §2 already do).

**Language and voice**
- [ ] Hindi is the default. The switch changes every string on the page.
- [ ] Listen works in Hindi on one real Android phone, or the fallback text shows.

**Journey**
- [ ] With JavaScript off, a user reaches the full result page.
- [ ] The pause step and the report list show at all three levels.
- [ ] The caveat shows at all three levels.
- [ ] The result page does not echo the full message.
- [ ] J1 (PRODUCT_SPEC §4) passes with a first-time tester.

**Weight**
- [ ] First load is 100 KB or less (ARCHITECTURE §8).
