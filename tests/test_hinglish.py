"""Hinglish / romanized Hindi scam pattern coverage."""

from __future__ import annotations

from app.rules import assess


def test_hinglish_pakka_munafa_and_otp():
    msg = "Bhai pakka munafa milega, otp bhejo aur aaj hi join karo"
    result = assess(msg)
    rules = {f.rule for f in result.findings}
    assert "guaranteed_returns" in rules
    assert "money_or_access" in rules
    assert "urgency" in rules
    assert result.level == "many"


def test_hinglish_fees_bharo_telegram():
    msg = "Registration fees bharo pehle, then telegram group join karo VIP"
    result = assess(msg)
    rules = {f.rule for f in result.findings}
    assert "money_or_access" in rules
    assert "private_channel" in rules
    assert result.level == "many"  # one strong


def test_hinglish_sebi_wala_jaldi():
    msg = "Ye sebi wala tip hai, jaldi karo limited seats"
    result = assess(msg)
    rules = {f.rule for f in result.findings}
    assert "fake_authority" in rules
    assert "urgency" in rules
    assert result.level == "some"


def test_hinglish_double_paisa_app_download():
    msg = "Double paisa guaranteed. App download karo abhi"
    result = assess(msg)
    rules = {f.rule for f in result.findings}
    assert "guaranteed_returns" in rules
    assert "private_channel" in rules
    assert result.level == "many"


def test_hinglish_educational_not_flagged():
    msg = "Kabhi bhi otp mat share karo. Private tip telegram ignore karo. Ye scam hai."
    result = assess(msg)
    assert result.findings == []
    assert result.level == "few"


def test_hinglish_bina_risk_anydesk():
    msg = "Bina risk returns, AnyDesk pe screen share karna hoga"
    result = assess(msg)
    rules = {f.rule for f in result.findings}
    assert "guaranteed_returns" in rules
    assert "money_or_access" in rules
    assert result.level == "many"
