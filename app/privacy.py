"""Mask sensitive tokens before any AI call (G3)."""

from __future__ import annotations

import re

# "OTP 123456" / "OTP: 123456"
_OTP = re.compile(r"(?i)\bOTP\b\s*[:\-]?\s*[0-9]{4,8}\b")

# Indian mobile numbers (+91 optional).
_PHONE = re.compile(r"(?<!\d)(?:\+91[\s-]*)?[6-9]\d{9}(?!\d)")

# Long account-like digit runs (9–18). Shorter money amounts stay.
_ACCOUNT = re.compile(r"(?<!\d)\d{9,18}(?!\d)")

_UPI = re.compile(r"\b[\w.-]{2,}@(?:upi|oksbi|okaxis|paytm|ybl|ibl)\b", re.I)


def mask_sensitive(text: str) -> str:
    """Mask phones, accounts, OTPs, and UPI ids. Money amounts stay."""
    if not text:
        return ""
    out = _OTP.sub("[OTP]", text)
    out = _UPI.sub("[UPI]", out)
    out = _PHONE.sub("[PHONE]", out)
    out = _ACCOUNT.sub("[ACCOUNT]", out)
    return out
