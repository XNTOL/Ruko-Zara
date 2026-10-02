"""All user-facing text (Hindi + English). Truth for wording.

Hindi strings that still need a native reader are marked with ``# REVIEW``.
Official phone numbers and URLs live here only (PRODUCT_SPEC G6).
"""

from __future__ import annotations

# Official links only. A person must verify these before submission (G6).
LINKS: dict[str, str] = {
    "helpline": "tel:1930",
    "cybercrime": "https://cybercrime.gov.in/",
    "scores": "https://scores.sebi.gov.in/",
    "sebi_check": "https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doRecognised=yes",
}

ALLOWED_URLS: frozenset[str] = frozenset(LINKS.values())

# UIUX_SPEC §7 copy deck + keys used by later screens.
STRINGS: dict[str, dict[str, str]] = {
    "hi": {
        "app_title": "रुको ज़रा",  # REVIEW
        "tagline": "पैसे भेजने से पहले, एक बार रुकें और जाँचें।",  # REVIEW
        "input_label": "जो संदेश आया है, उसे यहाँ चिपकाएँ",  # REVIEW
        "privacy_hint": (
            "OTP, बैंक खाता नंबर या पासवर्ड न डालें।"
            " आपका संदेश कहीं सेव नहीं होता।"
        ),  # REVIEW
        "btn_check": "जाँचें",  # REVIEW
        "btn_example": "उदाहरण देखें",  # REVIEW
        "btn_listen": "सुनें",  # REVIEW
        "btn_stop": "रोकें",  # REVIEW
        "btn_again": "दूसरा संदेश जाँचें",  # REVIEW
        "btn_copy": "चेतावनी कॉपी करें",  # REVIEW
        "copied": "कॉपी हो गया",  # REVIEW
        "loading": "जाँच जारी है…",  # REVIEW
        "section_reasons": "ये संकेत मिले",  # REVIEW
        "section_none": (
            "कोई साफ़ संकेत नहीं मिला।"
            " फिर भी पैसे भेजने से पहले परिवार में किसी से पूछें।"
        ),  # REVIEW
        "matched": "संदेश में मिला:",  # REVIEW
        "ai_label": "एआई द्वारा लिखा सारांश। इसमें गलती हो सकती है।",  # REVIEW
        "pause_title": "अभी रुकें",  # REVIEW
        "pause_1": "पैसे न भेजें और कोई लिंक न खोलें।",  # REVIEW
        "pause_2": "OTP, पिन या पासवर्ड किसी को न बताएं।",  # REVIEW
        "pause_3": "परिवार के किसी भरोसेमंद व्यक्ति से बात करें।",  # REVIEW
        "report_title": "पैसे चले गए हों या शक हो, तो यहाँ बताएँ",  # REVIEW
        "report_1930": "कॉल करें — साइबर ठगी हेल्पलाइन 1930",  # REVIEW
        "report_portal": "cybercrime.gov.in पर शिकायत दर्ज करें",  # REVIEW
        "report_scores": "सेबी SCORES पर शिकायत करें (ब्रोकर / म्यूचुअल फंड)",  # REVIEW
        "report_bank": "अपने बैंक या UPI ऐप को तुरंत बताएँ",  # REVIEW
        "report_bank_hint": "यह एक याद दिलाने वाला नोट है — कोई वेबसाइट लिंक नहीं।",  # REVIEW
        "report_call_hint": "फ़ोन पर टैप करें — डायल पैड खुलेगा।",  # REVIEW
        "sebi_found": (
            "संदेश में यह नंबर मिला: {number}।"
            " यह टूल इसकी जाँच नहीं कर सकता।"
            " सेबी की वेबसाइट पर खुद जाँचें।"
        ),  # REVIEW
        "sebi_claim_no_number": (
            "संदेश में सेबी रजिस्ट्रेशन का दावा है, पर कोई नंबर नहीं दिया गया।"
        ),  # REVIEW
        "btn_sebi": "सेबी की वेबसाइट पर जाँचें",  # REVIEW
        "card_title": "परिवार के ग्रुप के लिए चेतावनी",  # REVIEW
        "card_template": (
            "⚠️ रुको ज़रा! एक संदेश में ये चेतावनी संकेत मिले: {titles}।"
            " पैसे न भेजें, कोई लिंक न खोलें, OTP न बताएं।"
            " ठगी हो जाए तो 1930 पर बताएं।"
        ),  # REVIEW
        "voice_none": "इस फ़ोन पर आवाज़ उपलब्ध नहीं है।",  # REVIEW
        "error_empty": "पहले संदेश चिपकाएँ।",  # REVIEW
        "error_long": "संदेश बहुत लंबा है। मुख्य हिस्सा चिपकाएँ।",  # REVIEW
        "error_server": "कुछ गड़बड़ हो गई। कृपया दोबारा कोशिश करें।",  # REVIEW
        "footer": (
            "यह एक स्वतंत्र प्रोटोटाइप है,"
            " सेबी या एनएसडीएल की आधिकारिक सेवा नहीं।"
        ),  # REVIEW
        "about_link": "इस ऐप के बारे में",  # REVIEW
        "lang_hi": "हिन्दी",  # REVIEW
        "lang_en": "EN",
        "about_title": "इस ऐप के बारे में",  # REVIEW
        "about_how_heading": "यह कैसे काम करता है",  # REVIEW
        "about_how_body": (
            "आप एक संदेश चिपकाते हैं। नियम आम चेतावनी शब्दों को ढूँढते हैं।"
            " ऐप संकेत दिखाता है और पैसे भेजने से पहले रुकने को कहता है।"
            " नियम स्तर तय करते हैं। एआई केवल एक छोटा सारांश लिख सकता है।"
        ),  # REVIEW
        "about_storage_heading": "क्या सेव होता है",  # REVIEW
        "about_storage_body": (
            "कुछ नहीं। आपका संदेश सेव नहीं होता।"
            " कोई खाता नहीं, कोई कुकी नहीं।"
        ),  # REVIEW
        "about_limits_heading": "ईमानदार सीमाएँ",  # REVIEW
        "back_home": "जाँच पर वापस जाएँ",  # REVIEW
    },
    "en": {
        "app_title": "Ruko Zara",
        "tagline": "Before you send money, stop and check.",
        "input_label": "Paste the message you received",
        "privacy_hint": (
            "Do not paste an OTP, bank account number, or password."
            " Your message is not saved."
        ),
        "btn_check": "Check",
        "btn_example": "See an example",
        "btn_listen": "Listen",
        "btn_stop": "Stop",
        "btn_again": "Check another message",
        "btn_copy": "Copy warning",
        "copied": "Copied",
        "loading": "Checking…",
        "section_reasons": "Signs found",
        "section_none": (
            "No clear signs found."
            " Still, ask someone in your family before you send money."
        ),
        "matched": "Found in the message:",
        "ai_label": "AI-written summary. It can contain mistakes.",
        "pause_title": "Pause now",
        "pause_1": "Do not send money. Do not open any link.",
        "pause_2": "Do not tell anyone an OTP, PIN, or password.",
        "pause_3": "Talk to a family member you trust.",
        "report_title": "If money is gone, or you have a doubt, report here",
        "report_1930": "Call cyber fraud helpline 1930",
        "report_portal": "File a complaint at cybercrime.gov.in",
        "report_scores": "Open SEBI SCORES (broker or mutual fund complaint)",
        "report_bank": "Tell your bank or UPI app at once",
        "report_bank_hint": "Reminder only — not a website link.",
        "report_call_hint": "On a phone, tap to open the dial pad.",
        "sebi_found": (
            "This number was found in the message: {number}."
            " This tool cannot verify it."
            " Check it yourself on the SEBI website."
        ),
        "sebi_claim_no_number": (
            "The message claims SEBI registration but gives no number."
        ),
        "btn_sebi": "Check on the SEBI website",
        "card_title": "Warning for your family group",
        "card_template": (
            "⚠️ Ruko Zara! A message showed these warning signs: {titles}."
            " Do not send money, open any link, or share an OTP."
            " If you were cheated, call 1930."
        ),
        "voice_none": "Voice is not available on this phone.",
        "error_empty": "Paste a message first.",
        "error_long": "The message is too long. Paste the main part.",
        "error_server": "Something went wrong. Please try again.",
        "footer": (
            "This is an independent prototype."
            " It is not an official SEBI or NSDL service."
        ),
        "about_link": "About this app",
        "lang_hi": "हिन्दी",
        "lang_en": "EN",
        "about_title": "About this app",
        "about_how_heading": "How it works",
        "about_how_body": (
            "You paste a message. Rules look for common warning words."
            " The app shows the signs and asks you to pause before you send money."
            " Rules set the level. AI may write one short summary only."
        ),
        "about_storage_heading": "What is stored",
        "about_storage_body": (
            "Nothing. Your message is not saved."
            " There are no accounts and no cookies."
        ),
        "about_limits_heading": "Honest limits",
        "back_home": "Back to check",
    },
}

# PRODUCT_SPEC §9 — shown on /about.
ABOUT_LIMITS: dict[str, list[str]] = {
    "hi": [
        "नियम केवल शब्दों को पढ़ते हैं। नई चालें और गलत वर्तनी छूट सकती हैं।",  # REVIEW
        "यह टूल नहीं जानता कि संदेश किसने भेजा।",  # REVIEW
        "यह टूल सेबी नंबर की जाँच नहीं कर सकता। सेबी की अपनी खोज कर सकती है।",  # REVIEW
        "हिन्दी आवाज़ फ़ोन पर निर्भर करती है।",  # REVIEW
        "एआई सारांश में गलती हो सकती है।",  # REVIEW
        "मुफ़्त होस्ट को जागने में कुछ सेकंड लग सकते हैं।",  # REVIEW
    ],
    "en": [
        "Rules read words. New tricks and spelling changes can slip past.",
        "The tool does not know who sent the message.",
        "The tool cannot verify a SEBI number. SEBI's own search can.",
        "Hindi voice depends on the phone.",
        "The AI summary can contain mistakes.",
        "A free host may need a few seconds to wake up.",
    ],
}

# Moved from rules.py in T1.
LEVELS: dict[str, dict[str, str]] = {
    "many": {
        "hi": "बहुत से चेतावनी संकेत मिले",  # REVIEW
        "en": "Many warning signs found",
    },
    "some": {
        "hi": "कुछ चेतावनी संकेत मिले",  # REVIEW
        "en": "Some warning signs found",
    },
    "few": {
        "hi": "कम चेतावनी संकेत मिले",  # REVIEW
        "en": "Few warning signs found",
    },
    "no_text": {
        "hi": "संदेश खाली है",  # REVIEW
        "en": "No message text",
    },
}

CAVEAT: dict[str, str] = {
    "hi": (
        "यह टूल केवल आम चेतावनी शब्दों को देखता है।"
        " नई चालें छूट सकती हैं।"
        " यह नहीं जानता कि संदेश किसने भेजा।"
        " पैसे भेजने से पहले किसी भरोसेमंद व्यक्ति से पूछें।"
    ),  # REVIEW
    "en": (
        "This tool only looks for common warning words."
        " New tricks can slip past."
        " It does not know who sent the message."
        " Ask someone you trust before you send money."
    ),
}

# Rule titles and reasons. Keys match rule ids in rules.py.
TEXT: dict[str, dict[str, dict[str, str]]] = {
    "guaranteed_returns": {
        "title": {
            "hi": "पक्के मुनाफ़े का वादा",  # REVIEW
            "en": "Promise of sure profit",
        },
        "why": {
            "hi": (
                "बाज़ार में मुनाफ़े की कोई गारंटी नहीं होती।"
                " ऐसे वादे अक्सर ठगी का हिस्सा होते हैं।"
            ),  # REVIEW
            "en": (
                "No market return is certain."
                " Promises of sure profit are often part of a scam."
            ),
        },
    },
    "money_or_access": {
        "title": {
            "hi": "पैसे, OTP या ऐप पहुँच की माँग",  # REVIEW
            "en": "Ask for money, OTP, or app access",
        },
        "why": {
            "hi": (
                "भरोसेमंद संस्थाएँ इस तरह पहले से शुल्क,"
                " OTP या स्क्रीन शेयर नहीं माँगतीं।"
            ),  # REVIEW
            "en": (
                "Trusted bodies do not ask for fees up front,"
                " an OTP, or screen sharing in this way."
            ),
        },
    },
    "urgency": {
        "title": {
            "hi": "जल्दबाज़ी का दबाव",  # REVIEW
            "en": "Pressure to act at once",
        },
        "why": {
            "hi": (
                "जल्दी करने का दबाव सोचने का समय नहीं देता।"
                " ठग इसी जल्दबाज़ी का इस्तेमाल करते हैं।"
            ),  # REVIEW
            "en": (
                "Pressure to act at once leaves no time to think."
                " Scammers rely on that rush."
            ),
        },
    },
    "fake_authority": {
        "title": {
            "hi": "झूठा अधिकार या नाम",  # REVIEW
            "en": "False authority or name",
        },
        "why": {
            "hi": (
                "सेबी या सरकारी मंज़ूरी का दावा आसानी से लिखा जा सकता है।"
                " दावे की खुद जाँच करें।"
            ),  # REVIEW
            "en": (
                "Anyone can write a claim of SEBI or government approval."
                " Check the claim yourself."
            ),
        },
    },
    "private_channel": {
        "title": {
            "hi": "निजी ग्रुप या ऐप का लिंक",  # REVIEW
            "en": "Private group or app link",
        },
        "why": {
            "hi": (
                "निजी चैनल पर भेजे गए सुझाव की जाँच कठिन होती है।"
                " लिंक न खोलें।"
            ),  # REVIEW
            "en": (
                "Tips sent on a private channel are hard to check."
                " Do not open the link."
            ),
        },
    },
}

UI_KEYS: frozenset[str] = frozenset(STRINGS["en"].keys())
RULE_IDS: frozenset[str] = frozenset(TEXT.keys())


def t(lang: str, key: str) -> str:
    """Return one UI string. Falls back to English, then the key."""
    code = "hi" if lang == "hi" else "en"
    return STRINGS.get(code, STRINGS["en"]).get(key) or STRINGS["en"].get(key, key)
