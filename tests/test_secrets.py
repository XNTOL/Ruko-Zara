"""Repo must not ship live AI credentials (ARCHITECTURE §7)."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Common leaked-key shapes (Groq gsk_, OpenAI sk-, Bearer tokens in files).
_SECRET_SHAPES = re.compile(
    r"(?i)(?:"
    r"\bgsk_[A-Za-z0-9]{20,}\b|"
    r"\bsk-[A-Za-z0-9]{20,}\b|"
    r"Authorization:\s*Bearer\s+[A-Za-z0-9._\-]{20,}"
    r")"
)

_SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    "secrets",
}


def test_no_live_api_keys_in_tracked_tree():
    offenders: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in _SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".ico", ".pdf"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if _SECRET_SHAPES.search(text):
            offenders.append(str(path.relative_to(ROOT)))
    assert offenders == [], f"Possible secrets in: {offenders}"


def test_env_example_has_empty_key_slot():
    example = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "AI_API_KEY=" in example
    assert not re.search(r"(?m)^AI_API_KEY=\S+", example)


def test_gitignore_keeps_dotenv_out_of_git():
    ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in ignore
    assert ".env.*" in ignore or "*.env" in ignore
