"""Privacy masking tests (ARCHITECTURE §10)."""

from __future__ import annotations

from app.privacy import mask_sensitive


def test_masks_otp_keeps_words():
    out = mask_sensitive("Share your OTP 432198 now")
    assert "432198" not in out
    assert "[OTP]" in out


def test_masks_phone():
    out = mask_sensitive("Call me on 9876543210 today")
    assert "9876543210" not in out
    assert "[PHONE]" in out


def test_masks_account_number():
    out = mask_sensitive("Transfer to 123456789012 right away")
    assert "123456789012" not in out
    assert "[ACCOUNT]" in out


def test_money_amounts_stay():
    out = mask_sensitive("They asked for Rs 5000 and then ₹1200 more")
    assert "5000" in out
    assert "1200" in out


def test_upi_masked():
    out = mask_sensitive("Pay to demo@upi before joining")
    assert "demo@upi" not in out
    assert "[UPI]" in out
